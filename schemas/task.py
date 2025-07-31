from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    title: str
    description: str
    user_id: int
    status: str


class ResponseTask(CreateTask):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShortResponseTask(BaseModel):
    # id: int
    title: str
    description: str
    status: str


class PathUpdateTask(CreateTask):
    title: str | None = None
    description: str | None = None
    user_id: int | None = None
    status: str | None = None
