from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class ResponseUser(CreateUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdateUser(CreateUser):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
