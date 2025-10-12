from datetime import datetime
from todolist.core.models import Project, Task, TaskStatus
from todolist.storage.in_memory import InMemoryStorage
from todolist.exceptions import DuplicateError, ValidationError, LimitExceededError

class TodolistService:
    """Service layer containing all business logic."""

    def __init__(self, storage: InMemoryStorage, max_projects: int, max_tasks: int):
        self._storage = storage
        self._max_projects = max_projects
        self._max_tasks = max_tasks

    def create_project(self, name: str, description: str) -> Project:
        # Check against the maximum number of projects
        if len(self._storage.list_projects()) >= self._max_projects:
            raise LimitExceededError(f"Cannot create project. Maximum limit of {self._max_projects} reached.")
        if len(name) > 30 or len(description) > 150:
            raise ValidationError("Name or description exceeds character limits.")
        if self._storage.get_project_by_name(name):
            raise DuplicateError(f"Project with name '{name}' already exists.")
        
        return self._storage.create_project(name, description)

    def create_task(
        self, project_id: int, title: str, description: str, deadline_str: str | None
    ) -> Task:
        # Check against the maximum number of tasks for this project
        if len(self._storage.list_tasks_for_project(project_id)) >= self._max_tasks:
            raise LimitExceededError(f"Cannot create task. Maximum limit of {self._max_tasks} reached for this project.")
        
        if len(title) > 30 or len(description) > 150:
            raise ValidationError("Title or description exceeds character limits.")
        
        deadline = self._parse_deadline(deadline_str)
        return self._storage.create_task(project_id, title, description, deadline)

    def change_task_status(self, task_id: int, status: str) -> Task:
        if status not in ["todo", "doing", "done"]:
            raise ValidationError("Status must be one of 'todo', 'doing', or 'done'.")
        
        return self._storage.update_task_status(task_id, status)

    def _parse_deadline(self, deadline_str: str | None) -> datetime | None:
        """Helper to convert string to datetime object."""
        if not deadline_str:
            return None
        try:
            # Assumes YYYY-MM-DD format
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Invalid deadline format. Please use YYYY-MM-DD.")
    
    def get_task(self, task_id: int) -> Task:
        return self._storage.get_task(task_id) # Convenience method
    
    def edit_task(
        self,
        task_id: int,
        title: str,
        description: str,
        status: str,
        deadline_str: str | None,
    ) -> Task:
        # User story for editing a task
        if len(title) > 30 or len(description) > 150:
            raise ValidationError("Title or description exceeds character limits.")
        if status not in ["todo", "doing", "done"]: # [cite: 426]
            raise ValidationError("Status must be one of 'todo', 'doing', or 'done'.")
        
        deadline = self._parse_deadline(deadline_str) # Parse and validate
        return self._storage.update_task(task_id, title, description, status, deadline)
    
    def list_projects(self) -> list[Project]:
        return self._storage.list_projects()

    def list_tasks(self, project_id: int) -> list[Task]:
        return self._storage.list_tasks_for_project(project_id)