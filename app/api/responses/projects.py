from pydantic import BaseModel
from datetime import datetime

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read data from SQLAlchemy models