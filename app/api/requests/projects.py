from pydantic import BaseModel, Field

class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=30, description="Unique name of the project")
    description: str = Field(..., max_length=150, description="Short description of the project")

class UpdateProjectRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=30)
    description: str | None = Field(None, max_length=150)