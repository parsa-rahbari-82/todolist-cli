from pydantic import BaseModel
from datetime import datetime, date

class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    status: str
    deadline: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True