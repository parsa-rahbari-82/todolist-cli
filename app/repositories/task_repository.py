from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.exceptions.repository_exceptions import NotFoundError

class TaskRepository:
    """Repository for all Task-related database operations."""

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, task_id: int) -> Task:
        """Get a task by its ID."""
        task = self._session.get(Task, task_id)
        if not task:
            raise NotFoundError(f"Task with id {task_id} not found.")
        return task

    def list_by_project_id(self, project_id: int) -> list[Task]:
        """List all tasks for a given project."""
        # Ensure project exists first
        if not self._session.get(Project, project_id):
             raise NotFoundError(f"Project with id {project_id} not found.")
        
        return list(self._session.execute(
            select(Task).where(Task.project_id == project_id)
        ).scalars())

    def create(
        self, project_id: int, title: str, description: str, deadline: datetime | None
    ) -> Task:
        """Create a new task."""
        # Ensure project exists
        if not self._session.get(Project, project_id):
             raise NotFoundError(f"Project with id {project_id} not found.")

        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline
        )
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def update(
        self,
        task_id: int,
        title: str,
        description: str,
        status: TaskStatus,
        deadline: datetime | None,
    ) -> Task:
        """Update all fields of an existing task."""
        task = self.get_by_id(task_id)
        task.title = title
        task.description = description
        task.status = status
        task.deadline = deadline
        self._session.commit()
        self._session.refresh(task)
        return task

    def update_status(self, task_id: int, status: TaskStatus) -> Task:
        """Update only the status of a task."""
        task = self.get_by_id(task_id)
        task.status = status
        self._session.commit()
        self._session.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        """Delete a task."""
        task = self.get_by_id(task_id)
        self._session.delete(task)
        self._session.commit()

    def find_overdue_tasks(self) -> list[Task]:
        """Finds all tasks that are past their deadline and not 'done'."""
        now = datetime.utcnow()
        return list(self._session.execute(
            select(Task).where(
                Task.deadline < now,
                Task.status != "done"
            )
        ).scalars())