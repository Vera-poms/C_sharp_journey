from typing import Any

from pydantic import BaseModel


class ModuleSummary(BaseModel):
    id: int
    number: int
    title: str
    description: str
    lesson_count: int
    completed_count: int


class LessonRef(BaseModel):
    id: int
    label: str
    title: str
    completed: bool


class ModuleDetail(BaseModel):
    id: int
    number: int
    title: str
    lessons: list[LessonRef]


class LessonDetail(BaseModel):
    id: int
    label: str
    title: str
    subtitle: str
    completed: bool
    lab_passed: bool
    watched_seconds: int
    module: ModuleDetail
    reading: list[dict[str, Any]]
    codealong: dict[str, Any] | None
    video: dict[str, Any] | None
    resources: list[dict[str, Any]]
    lab: dict[str, Any] | None


class Stats(BaseModel):
    lessons_completed: int
    lessons_total: int
    modules_started: int
    modules_total: int
    labs_passed: int
    watch_seconds: int


class WatchIn(BaseModel):
    seconds: int
    position: int | None = None


class WatchOut(BaseModel):
    watched_seconds: int
    position_seconds: int


class CodeIn(BaseModel):
    code: str


class RunResult(BaseModel):
    ok: bool
    output: str


class CliIn(BaseModel):
    session: str
    command: str


class CliResult(RunResult):
    cwd: str


class SubmitResult(RunResult):
    lesson_completed: bool


class NextLesson(BaseModel):
    lesson_id: int
