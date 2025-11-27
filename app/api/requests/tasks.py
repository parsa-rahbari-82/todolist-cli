from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=30)
    description: str = Field(..., max_length=150)
    deadline: date | None = None

class UpdateTaskRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=30)
    description: str | None = Field(None, max_length=150)
    status: Literal["todo", "doing", "done"] | None = None
    deadline: date | None = None