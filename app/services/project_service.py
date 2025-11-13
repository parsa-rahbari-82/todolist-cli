from app.repositories.project_repository import ProjectRepository
from app.models.project import Project
from app.exceptions.service_exceptions import LimitExceededError, ValidationError

class ProjectService:
    """Service layer for Project business logic."""

    def __init__(self, repo: ProjectRepository, max_projects: int):
        self._repo = repo
        self._max_projects = max_projects

    def create_project(self, name: str, description: str) -> Project:
        """Create a new project, enforcing business rules."""
        if len(self._repo.list_all()) >= self._max_projects:
            raise LimitExceededError(f"Cannot create project. Maximum limit of {self._max_projects} reached.")
        
        if len(name) > 30 or len(description) > 150:
            raise ValidationError("Name (max 30) or description (max 150) exceeds character limits.")
        
        return self._repo.create(name, description)

    def edit_project(self, project_id: int, name: str, description: str) -> Project:
        """Update a project, enforcing business rules."""
        if len(name) > 30 or len(description) > 150:
            raise ValidationError("Name (max 30) or description (max 150) exceeds character limits.")
            
        return self._repo.update(project_id, name, description)
    
    def list_projects(self) -> list[Project]:
        """List all projects."""
        return self._repo.list_all()

    def delete_project(self, project_id: int) -> None:
        """Delete a project and all its tasks (via cascade)."""
        self._repo.delete(project_id)

    def get_project(self, project_id: int) -> Project:
        """Get a single project by ID."""
        return self._repo.get_by_id(project_id)