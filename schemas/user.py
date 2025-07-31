from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class ResponseUser(CreateUser):
    id: int

    model_config = ConfigDict(from_attributes=True)
