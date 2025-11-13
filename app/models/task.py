from __future__ import annotations
from datetime import datetime
from typing import Literal
from sqlalchemy import String, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.project import Project

TaskStatus = Literal["todo", "doing", "done"]

class Task(Base):
    """ORM Model for a Task."""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(150))
    status: Mapped[TaskStatus] = mapped_column(String(5), default="todo")
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    
    # A Task belongs to one Project
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    def __str__(self) -> str:
        deadline_str = self.deadline.strftime('%Y-%m-%d') if self.deadline else "None"
        return (
            f"  - Task {self.id}: {self.title} "
            f"[{self.status.upper()}] (Project: {self.project_id}) (Deadline: {deadline_str})"
        )