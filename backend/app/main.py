import logging
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import func, select, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, selectinload

from . import runner, schemas
from .database import Base, SessionLocal, engine, get_db
from .models import LabSubmission, Lesson, LessonProgress, Module, WatchTime
from .seed import seed_if_empty, sync_content, sync_links

log = logging.getLogger("csharp_journey")


def wait_for_db(attempts: int = 30, delay: float = 1.0) -> None:
    for attempt in range(1, attempts + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            log.info("Waiting for database (%d/%d)", attempt, attempts)
            time.sleep(delay)
    raise RuntimeError("Database did not become available")


@asynccontextmanager
async def lifespan(_: FastAPI):
    wait_for_db()
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        # create_all doesn't alter existing tables; add columns introduced later.
        conn.execute(text("ALTER TABLE lessons ADD COLUMN IF NOT EXISTS resources JSONB"))
        conn.execute(text("ALTER TABLE watch_time ADD COLUMN IF NOT EXISTS position INTEGER DEFAULT 0"))
    with SessionLocal() as db:
        seed_if_empty(db)
        sync_content(db)
        sync_links(db)
    yield


app = FastAPI(title="C# Journey API", lifespan=lifespan)


@app.exception_handler(runner.RunnerUnavailable)
def runner_unavailable(_, exc):
    return JSONResponse({"detail": "The code runner is unavailable."}, status_code=503)


def completed_ids(db: Session) -> set[int]:
    return set(db.scalars(select(LessonProgress.lesson_id)))


def get_lesson_or_404(db: Session, lesson_id: int) -> Lesson:
    lesson = db.scalar(
        select(Lesson)
        .where(Lesson.id == lesson_id)
        .options(selectinload(Lesson.module).selectinload(Module.lessons))
    )
    if lesson is None:
        raise HTTPException(404, "Lesson not found")
    return lesson


def module_detail(module: Module, done: set[int]) -> schemas.ModuleDetail:
    return schemas.ModuleDetail(
        id=module.id,
        number=module.number,
        title=module.title,
        lessons=[
            schemas.LessonRef(
                id=l.id,
                label=f"{module.number}.{l.number}",
                title=l.title,
                completed=l.id in done,
            )
            for l in module.lessons
        ],
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/stats", response_model=schemas.Stats)
def stats(db: Session = Depends(get_db)):
    done = completed_ids(db)
    modules = db.scalars(select(Module).options(selectinload(Module.lessons))).all()
    return schemas.Stats(
        lessons_completed=len(done),
        lessons_total=sum(len(m.lessons) for m in modules),
        modules_started=sum(1 for m in modules if any(l.id in done for l in m.lessons)),
        modules_total=len(modules),
        labs_passed=db.scalar(
            select(func.count(func.distinct(LabSubmission.lesson_id))).where(LabSubmission.passed)
        )
        or 0,
        watch_seconds=db.scalar(select(func.coalesce(func.sum(WatchTime.seconds), 0))) or 0,
    )


@app.get("/api/modules",response_model=list[schemas.ModuleSummary])
def list_modules(db: Session = Depends(get_db)):
    done = completed_ids(db)
    modules = db.scalars(
        select(Module).order_by(Module.number).options(selectinload(Module.lessons))
    ).all()
    return [
        schemas.ModuleSummary(
            id=m.id,
            number=m.number,
            title=m.title,
            description=m.description,
            lesson_count=len(m.lessons),
            completed_count=sum(1 for l in m.lessons if l.id in done),
        )
        for m in modules
    ]


def first_unfinished(lessons: list[Lesson], done: set[int]) -> Lesson | None:
    return next((l for l in lessons if l.id not in done), lessons[0] if lessons else None)


@app.get("/api/modules/{module_id}/start", response_model=schemas.NextLesson)
def start_module(module_id: int, db: Session = Depends(get_db)):
    module = db.scalar(
        select(Module).where(Module.id == module_id).options(selectinload(Module.lessons))
    )
    if module is None or not module.lessons:
        raise HTTPException(404, "Module not found")
    return schemas.NextLesson(lesson_id=first_unfinished(module.lessons, completed_ids(db)).id)


@app.get("/api/next-lesson", response_model=schemas.NextLesson)
def next_lesson(db: Session = Depends(get_db)):
    done = completed_ids(db)
    lessons = db.scalars(
        select(Lesson).join(Module).order_by(Module.number, Lesson.number)
    ).all()
    lesson = first_unfinished(lessons, done)
    if lesson is None:
        raise HTTPException(404, "No lessons")
    return schemas.NextLesson(lesson_id=lesson.id)


@app.get("/api/lessons/{lesson_id}", response_model=schemas.LessonDetail)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = get_lesson_or_404(db, lesson_id)
    done = completed_ids(db)
    passed = db.scalar(
        select(func.count())
        .select_from(LabSubmission)
        .where(LabSubmission.lesson_id == lesson_id, LabSubmission.passed)
    )
    return schemas.LessonDetail(
        id=lesson.id,
        label=f"{lesson.module.number}.{lesson.number}",
        title=lesson.title,
        subtitle=lesson.subtitle,
        completed=lesson.id in done,
        lab_passed=bool(passed),
        watched_seconds=watch.seconds if (watch := db.get(WatchTime, lesson_id)) else 0,
        module=module_detail(lesson.module, done),
        reading=lesson.reading,
        codealong=lesson.codealong,
        video=lesson.video,
        resources=lesson.resources or [],
        lab=lesson.lab,
    )


@app.post("/api/lessons/{lesson_id}/complete", status_code=204)
def complete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    get_lesson_or_404(db, lesson_id)
    if db.get(LessonProgress, lesson_id) is None:
        db.add(LessonProgress(lesson_id=lesson_id))
        db.commit()


@app.delete("/api/lessons/{lesson_id}/complete", status_code=204)
def uncomplete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    progress = db.get(LessonProgress, lesson_id)
    if progress is not None:
        db.delete(progress)
        db.commit()


def watch_out(row: WatchTime | None) -> schemas.WatchOut:
    return schemas.WatchOut(
        watched_seconds=row.seconds if row else 0,
        position_seconds=(row.position or 0) if row else 0,
    )


@app.get("/api/lessons/{lesson_id}/watch", response_model=schemas.WatchOut)
def get_watch_time(lesson_id: int, db: Session = Depends(get_db)):
    get_lesson_or_404(db, lesson_id)
    return watch_out(db.get(WatchTime, lesson_id))


@app.post("/api/lessons/{lesson_id}/watch", response_model=schemas.WatchOut)
def add_watch_time(lesson_id: int, body: schemas.WatchIn, db: Session = Depends(get_db)):
    """Add seconds of video watched (and remember the playback position); reported in small batches."""
    get_lesson_or_404(db, lesson_id)
    # A single report can't plausibly exceed a few hours; ignore junk rather than corrupt the total.
    seconds = max(0, min(body.seconds, 6 * 3600))
    row = db.get(WatchTime, lesson_id)
    if row is None:
        row = WatchTime(lesson_id=lesson_id, seconds=0, position=0)
        db.add(row)
    row.seconds += seconds
    if body.position is not None:
        row.position = max(0, body.position)
    db.commit()
    return watch_out(row)


@app.post("/api/lessons/{lesson_id}/codealong/run",response_model=schemas.RunResult)
def run_codealong(lesson_id: int, body: schemas.CodeIn, db: Session = Depends(get_db)):
    lesson = get_lesson_or_404(db, lesson_id)
    if not lesson.codealong:
        raise HTTPException(404, "This lesson has no code-along")
    ok, output = runner.run_code(body.code)
    return schemas.RunResult(ok=ok, output=output)


@app.post("/api/lessons/{lesson_id}/scratch/run", response_model=schemas.RunResult)
def run_scratch(lesson_id: int, body: schemas.CodeIn, db: Session = Depends(get_db)):
    """Free-form practice editor shown beside the Reading and Video tabs."""
    get_lesson_or_404(db, lesson_id)
    ok, output = runner.run_code(body.code)
    return schemas.RunResult(ok=ok, output=output)


@app.post("/api/lessons/{lesson_id}/cli/run", response_model=schemas.CliResult)
def run_cli(lesson_id: int, body: schemas.CliIn, db: Session = Depends(get_db)):
    """Terminal beside the lesson, for the `dotnet ...` commands the lessons teach."""
    get_lesson_or_404(db, lesson_id)
    ok, output, cwd = runner.run_cli(body.session, body.command)
    return schemas.CliResult(ok=ok, output=output, cwd=cwd)


@app.post("/api/lessons/{lesson_id}/lab/run", response_model=schemas.RunResult)
def run_lab(lesson_id: int, body: schemas.CodeIn, db: Session = Depends(get_db)):
    lesson = get_lesson_or_404(db, lesson_id)
    if not lesson.lab:
        raise HTTPException(404, "This lesson has no lab")
    ok, output = runner.run_code(body.code)
    return schemas.RunResult(ok=ok, output=output)


@app.post("/api/lessons/{lesson_id}/lab/submit", response_model=schemas.SubmitResult)
def submit_lab(lesson_id: int, body: schemas.CodeIn, db: Session = Depends(get_db)):
    lesson = get_lesson_or_404(db, lesson_id)
    if not lesson.lab:
        raise HTTPException(404, "This lesson has no lab")
    ok, output = runner.check_lab(body.code, lesson.lab)
    db.add(LabSubmission(lesson_id=lesson_id, code=body.code, passed=ok, output=output))
    if ok and db.get(LessonProgress, lesson_id) is None:
        db.add(LessonProgress(lesson_id=lesson_id))
    db.commit()
    return schemas.SubmitResult(
        ok=ok,
        output="✓ All tests passed! Great work." if ok else output,
        lesson_completed=ok,
    )
