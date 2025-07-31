from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    title: str
    description: str
    assignee: str
    status: str


class ResponseTask(CreateTask):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PathUpdateTask(CreateTask):
    title: str | None = None
    description: str | None = None
    assignee: str | None = None
    status: str | None = None
