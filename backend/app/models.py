from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer, unique=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module", order_by="Lesson.number", cascade="all, delete-orphan"
    )


class Lesson(Base):
    __tablename__ = "lessons"
    __table_args__ = (UniqueConstraint("module_id", "number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    subtitle: Mapped[str] = mapped_column(Text, default="")
    # Structured lesson content, see seed_content.py for the shapes.
    reading: Mapped[list] = mapped_column(JSONB, default=list)
    codealong: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    video: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    lab: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # External links (Microsoft Learn, W3Schools, ...), see seed_resources.py.
    resources: Mapped[list] = mapped_column(JSONB, default=list)

    module: Mapped[Module] = relationship(back_populates="lessons")
    progress: Mapped["LessonProgress | None"] = relationship(
        back_populates="lesson", uselist=False, cascade="all, delete-orphan"
    )
    submissions: Mapped[list["LabSubmission"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )


class LessonProgress(Base):
    """One row per completed lesson (single-learner app, no accounts)."""

    __tablename__ = "lesson_progress"

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True
    )
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    lesson: Mapped[Lesson] = relationship(back_populates="progress")


class WatchTime(Base):
    """Seconds spent watching a lesson's video, on the site or on YouTube."""

    __tablename__ = "watch_time"

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True
    )
    seconds: Mapped[int] = mapped_column(Integer, default=0)
    # Where the embedded player last was, so the video resumes there.
    position: Mapped[int] = mapped_column(Integer, default=0)


class LabSubmission(Base):
    __tablename__ = "lab_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(Text)
    passed: Mapped[bool] = mapped_column(Boolean)
    output: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    lesson: Mapped[Lesson] = relationship(back_populates="submissions")
