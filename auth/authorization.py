from ast import stmt
from typing import Annotated
from fastapi import Depends, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
from schemas.user import LoginUser, RegisterUser, ResponseUser
from auth.dependencies import register_helper
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=ResponseUser)
async def register(
    data: Annotated[
        RegisterUser, Body(description="Данные пользователя для регистрации")
    ],
    session: AsyncSession = Depends(get_session),
):
    return await register_helper(data=data, session=session)
