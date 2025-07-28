from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CreateTask(BaseModel):
    title: str
    description: str
    assignee: str
    status: str


class ResponseTask(CreateTask):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
