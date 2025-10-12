from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

TaskStatus = Literal["todo", "doing", "done"]

@dataclass
class Task:
    """Represents a single task in a project."""
    id: int
    project_id: int
    title: str
    description: str
    status: TaskStatus = "todo"
    deadline: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        deadline_str = self.deadline.strftime('%Y-%m-%d') if self.deadline else "None"
        return (
            f"  - Task {self.id}: {self.title} "
            f"[{self.status.upper()}] (Deadline: {deadline_str})"
        )

@dataclass
class Project:
    """Represents a project that contains tasks."""
    id: int
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __str__(self) -> str:
        return f"Project {self.id}: {self.name} - {self.description}"
