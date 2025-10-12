from datetime import datetime
from todolist.core.models import Project, Task
from todolist.exceptions import NotFoundError

class InMemoryStorage:
    """A simple in-memory storage for projects and tasks."""
    
    def __init__(self) -> None:
        self._projects: dict[int, Project] = {}
        self._tasks: dict[int, Task] = {}
        self._project_counter: int = 0
        self._task_counter: int = 0

    # --- Project Methods ---

    def create_project(self, name: str, description: str) -> Project:
        self._project_counter += 1
        project = Project(id=self._project_counter, name=name, description=description)
        self._projects[project.id] = project
        return project

    def list_projects(self) -> list[Project]:
        return sorted(self._projects.values(), key=lambda p: p.created_at)

    def get_project(self, project_id: int) -> Project:
        if project_id not in self._projects:
            raise NotFoundError(f"Project with id {project_id} not found.")
        return self._projects[project_id]

    def get_project_by_name(self, name: str) -> Project | None:
        return next((p for p in self._projects.values() if p.name == name), None)

    def update_project(self, project_id: int, name: str, description: str) -> Project:
        project = self.get_project(project_id)
        project.name = name
        project.description = description
        return project

    def delete_project(self, project_id: int) -> None:
        project = self.get_project(project_id) # Ensures project exists
        # Cascade delete: remove all tasks associated with the project
        tasks_to_delete = [
            task_id for task_id, task in self._tasks.items() 
            if task.project_id == project_id
        ]
        for task_id in tasks_to_delete:
            del self._tasks[task_id]
        del self._projects[project.id]

    # --- Task Methods ---

    def create_task(self, project_id: int, title: str, description: str, deadline: datetime | None) -> Task:
        self.get_project(project_id) # Ensure project exists
        self._task_counter += 1
        task = Task(
            id=self._task_counter,
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise NotFoundError(f"Task with id {task_id} not found.")
        return self._tasks[task_id]

    def list_tasks_for_project(self, project_id: int) -> list[Task]:
        self.get_project(project_id) # Ensure project exists
        return [
            task for task in self._tasks.values() 
            if task.project_id == project_id
        ]
        
    def update_task_status(self, task_id: int, status: str) -> Task:
        task = self.get_task(task_id)
        task.status = status
        return task
    
    def update_task(
        self,
        task_id: int,
        title: str,
        description: str,
        status: str,
        deadline: datetime | None,
    ) -> Task:
        task = self.get_task(task_id)
        task.title = title
        task.description = description
        task.status = status
        task.deadline = deadline
        return task