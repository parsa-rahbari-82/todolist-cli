from fastapi import FastAPI
from app.api.controllers import projects_controller, tasks_controller

app = FastAPI(
    title="ToDo List API",
    description="Phase 3 Web API Implementation",
    version="1.0.0"
)

# Include Routers
app.include_router(projects_controller.router)
app.include_router(tasks_controller.router)
app.include_router(tasks_controller.task_router) # The global task operations

@app.get("/")
def root():
    return {"message": "Welcome to ToDo List Web API"}