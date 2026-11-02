from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Lesson, Module
from .seed_content import COMING_SOON, MODULES, RICH_LESSONS
from .seed_resources import VIDEOS, resources_for


def seed_if_empty(db: Session) -> None:
    if db.scalar(select(Module.id).limit(1)) is not None:
        return

    for m_number, m in enumerate(MODULES, start=1):
        module = Module(number=m_number, title=m["title"], description=m["description"])
        for l_number, title in enumerate(m["lessons"], start=1):
            rich = RICH_LESSONS.get((m_number, l_number), {})
            module.lessons.append(
                Lesson(
                    number=l_number,
                    title=title,
                    subtitle=rich.get("subtitle", ""),
                    reading=rich.get("reading", COMING_SOON),
                    codealong=rich.get("codealong"),
                    lab=rich.get("lab"),
                )
            )
        db.add(module)
    db.commit()


def sync_content(db: Session) -> None:
    """Refresh lesson text, code-alongs and labs from seed_content.py on every start.

    Seeding only runs on an empty database, so this keeps already-seeded lessons
    in step with the course content. Progress and lab submissions are untouched.
    """
    rows = db.execute(select(Module.number, Lesson).join(Lesson.module)).all()
    for m_number, lesson in rows:
        rich = RICH_LESSONS.get((m_number, lesson.number))
        if rich is None:
            continue
        lesson.subtitle = rich.get("subtitle", "")
        lesson.reading = rich.get("reading", COMING_SOON)
        lesson.codealong = rich.get("codealong")
        lesson.lab = rich.get("lab")
    db.commit()


def sync_links(db: Session) -> None:
    """Refresh videos and resources from seed_resources.py on every start.

    Seeding only runs on an empty database, so this keeps already-seeded
    lessons in step with the link catalog without touching progress or content.
    """
    rows = db.execute(select(Module.number, Lesson).join(Lesson.module)).all()
    for m_number, lesson in rows:
        key = (m_number, lesson.number)
        lesson.video = VIDEOS.get(key)
        lesson.resources = resources_for(key)
    db.commit()
