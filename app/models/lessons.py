from __future__ import annotations

from typing import List

from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


lesson_group_assoc_table = Table(
    "lesson_group_assoc_table",
    Base.metadata,
    Column(
        "group_id",
        ForeignKey("groups.id"),
        primary_key=True
    ),
    Column(
        "lesson_id",
        ForeignKey("lessons.id"),
        primary_key=True
    )
)


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    groups: Mapped[List["app.models.group.Group"]] = relationship("app.models.group.Group",
                                                                  secondary=lesson_group_assoc_table,
                                                                  back_populates="lessons")

    def __repr__(self):
        group_names = ', '.join([group.name for group in self.groups])
        return f"Lesson: {self.title} (Groups: {group_names})"
