from todolist.core.models import Project, Task, TaskStatus
from todolist.storage.in_memory import InMemoryStorage
from todolist.exceptions import DuplicateError, ValidationError

class TodolistService:
    """Service layer containing all business logic."""

    def __init__(self, storage: InMemoryStorage):
        self._storage = storage

    def create_project(self, name: str, description: str) -> Project:
        if len(name) > 30 or len(description) > 150:
            raise ValidationError("Name or description exceeds character limits.")
        if self._storage.get_project_by_name(name):
            raise DuplicateError(f"Project with name '{name}' already exists.")
        
        return self._storage.create_project(name, description)

    def create_task(self, project_id: int, title: str, description: str) -> Task:
        if len(title) > 30 or len(description) > 150:
            raise ValidationError("Title or description exceeds character limits.")
        
        return self._storage.create_task(project_id, title, description)

    def change_task_status(self, task_id: int, status: str) -> Task:
        if status not in ["todo", "doing", "done"]:
            raise ValidationError("Status must be one of 'todo', 'doing', or 'done'.")
        
        return self._storage.update_task_status(task_id, status)

    def list_projects(self) -> list[Project]:
        return self._storage.list_projects()

    def list_tasks(self, project_id: int) -> list[Task]:
        return self._storage.list_tasks_for_project(project_id)