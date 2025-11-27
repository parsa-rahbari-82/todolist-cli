from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db_session
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService
from app.api.requests.projects import CreateProjectRequest, UpdateProjectRequest
from app.api.responses.projects import ProjectResponse
from app.exceptions.base import TodolistError

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_project_service(db: Session = Depends(get_db_session)) -> ProjectService:
    repo = ProjectRepository(db)
    # Hardcoding limits for now as per env variables logic, or you can fetch os.getenv here
    return ProjectService(repo, max_projects=10)

@router.get("/", response_model=list[ProjectResponse])
def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.list_projects()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    try:
        return service.get_project(project_id)
    except TodolistError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: CreateProjectRequest, 
    service: ProjectService = Depends(get_project_service)
):
    try:
        return service.create_project(data.name, data.description)
    except TodolistError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int, 
    data: UpdateProjectRequest, 
    service: ProjectService = Depends(get_project_service)
):
    try:
        # Pydantic sends None for unset fields, handling partial updates requires logic in Service
        # For simplicity, we assume PUT sends all fields or we handle it here.
        # Ideally, Service.edit_project should handle partials if arguments are None.
        # Here we pass existing values if new ones are None, simulating a PATCH behavior often mixed in simple APIs
        current = service.get_project(project_id)
        name = data.name if data.name is not None else current.name
        description = data.description if data.description is not None else current.description
        
        return service.edit_project(project_id, name, description)
    except TodolistError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    try:
        service.delete_project(project_id)
    except TodolistError as e:
        raise HTTPException(status_code=404, detail=str(e))