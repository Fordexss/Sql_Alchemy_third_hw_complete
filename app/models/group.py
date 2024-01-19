from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from .lessons import lesson_group_assoc_table, Lesson


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    lessons: Mapped[List[Lesson]] = relationship(Lesson, secondary=lesson_group_assoc_table, back_populates="groups")

    def __repr__(self):
        return f"Group: {self.name}"
