from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.project import Project
from app.exceptions.repository_exceptions import NotFoundError, DuplicateError

class ProjectRepository:
    """Repository for all Project-related database operations."""

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, project_id: int) -> Project:
        """Get a project by its ID."""
        project = self._session.get(Project, project_id)
        if not project:
            raise NotFoundError(f"Project with id {project_id} not found.")
        return project

    def get_by_name(self, name: str) -> Project | None:
        """Get a project by its unique name."""
        return self._session.execute(
            select(Project).where(Project.name == name)
        ).scalar_one_or_none()

    def list_all(self) -> list[Project]:
        """List all projects."""
        return list(self._session.execute(
            select(Project).order_by(Project.created_at)
        ).scalars())

    def create(self, name: str, description: str) -> Project:
        """Create a new project."""
        if self.get_by_name(name):
            raise DuplicateError(f"Project with name '{name}' already exists.")
        
        project = Project(name=name, description=description)
        self._session.add(project)
        self._session.commit()
        self._session.refresh(project)
        return project

    def update(self, project_id: int, name: str, description: str) -> Project:
        """Update an existing project."""
        project = self.get_by_id(project_id)
        
        # Check if new name is taken by another project
        existing_with_name = self.get_by_name(name)
        if existing_with_name and existing_with_name.id != project_id:
            raise DuplicateError(f"Project name '{name}' is already in use.")

        project.name = name
        project.description = description
        self._session.commit()
        self._session.refresh(project)
        return project

    def delete(self, project_id: int) -> None:
        """Delete a project."""
        project = self.get_by_id(project_id)
        self._session.delete(project)
        self._session.commit()