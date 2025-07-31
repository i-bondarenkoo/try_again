from pydantic import BaseModel, ConfigDict, EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.task import ShortResponseTask


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class ResponseUser(CreateUser):
    id: int
    tasks: list["ShortResponseTask"]
    model_config = ConfigDict(from_attributes=True)


class UpdateUser(CreateUser):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
