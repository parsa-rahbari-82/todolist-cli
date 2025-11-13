from datetime import datetime
from app.repositories.task_repository import TaskRepository
from app.models.task import Task, TaskStatus
from app.exceptions.service_exceptions import LimitExceededError, ValidationError

class TaskService:
    """Service layer for Task business logic."""

    def __init__(self, repo: TaskRepository, max_tasks_per_project: int):
        self._repo = repo
        self._max_tasks = max_tasks_per_project

    def _parse_deadline(self, deadline_str: str | None) -> datetime | None:
        """Helper to convert string to datetime object."""
        if not deadline_str:
            return None
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Invalid deadline format. Please use YYYY-MM-DD.")
    
    def _validate_status(self, status: str) -> TaskStatus:
        """Helper to validate task status."""
        if status not in ["todo", "doing", "done"]:
            raise ValidationError("Status must be one of 'todo', 'doing', or 'done'.")
        return status # type: ignore

    def create_task(
        self, project_id: int, title: str, description: str, deadline_str: str | None
    ) -> Task:
        """Create a new task, enforcing business rules."""
        if len(self._repo.list_by_project_id(project_id)) >= self._max_tasks:
            raise LimitExceededError(f"Cannot create task. Maximum limit of {self._max_tasks} reached for this project.")
        
        if len(title) > 30 or len(description) > 150:
            raise ValidationError("Title (max 30) or description (max 150) exceeds character limits.")
        
        deadline = self._parse_deadline(deadline_str)
        return self._repo.create(project_id, title, description, deadline)

    def edit_task(
        self,
        task_id: int,
        title: str,
        description: str,
        status_str: str,
        deadline_str: str | None,
    ) -> Task:
        """Update a task, enforcing business rules."""
        if len(title) > 30 or len(description) > 150:
            raise ValidationError("Title (max 30) or description (max 150) exceeds character limits.")
        
        status = self._validate_status(status_str)
        deadline = self._parse_deadline(deadline_str)
        
        return self._repo.update(task_id, title, description, status, deadline)

    def change_task_status(self, task_id: int, status_str: str) -> Task:
        """Update a task's status."""
        status = self._validate_status(status_str)
        return self._repo.update_status(task_id, status)

    def get_task(self, task_id: int) -> Task:
        """Get a single task by ID."""
        return self._repo.get_by_id(task_id)

    def list_tasks(self, project_id: int) -> list[Task]:
        """List all tasks for a project."""
        return self._repo.list_by_project_id(project_id)

    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        self._repo.delete(task_id)