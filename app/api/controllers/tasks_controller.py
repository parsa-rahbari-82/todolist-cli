from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db_session
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.api.requests.tasks import CreateTaskRequest, UpdateTaskRequest
from app.api.responses.tasks import TaskResponse
from app.exceptions.base import TodolistError

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])

def get_task_service(db: Session = Depends(get_db_session)) -> TaskService:
    repo = TaskRepository(db)
    return TaskService(repo, max_tasks_per_project=20)

@router.get("/", response_model=list[TaskResponse])
def list_tasks(project_id: int, service: TaskService = Depends(get_task_service)):
    try:
        return service.list_tasks(project_id)
    except TodolistError as e:
         raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    data: CreateTaskRequest, 
    service: TaskService = Depends(get_task_service)
):
    try:
        # Convert date to string as Service currently expects strings or update service to accept date objects
        deadline_str = data.deadline.strftime("%Y-%m-%d") if data.deadline else None
        return service.create_task(project_id, data.title, data.description, deadline_str)
    except TodolistError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Note: Task updates might need a separate router if you want /tasks/{task_id}
# But typically tasks belong to projects. Let's assume a general /tasks endpoint for updates/deletes
# to avoid deep nesting issues in URL design.

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        service.delete_task(task_id)
    except TodolistError as e:
        raise HTTPException(status_code=404, detail=str(e))