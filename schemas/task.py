from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.user import ResponseShortUser


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


class ResponseTaskWithUser(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    user: "ResponseShortUser"


class PathUpdateTask(CreateTask):
    title: str | None = None
    description: str | None = None
    user_id: int | None = None
    status: str | None = None
