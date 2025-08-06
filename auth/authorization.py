from typing import Annotated
from fastapi import Depends, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
from schemas.user import LoginUser, RegisterUser, ResponseUser
from auth.dependencies import register_helper, authenticate_user_helper
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from auth.jwt import create_access_token
from schemas.token import TokenResponse

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


@router.post("/login", response_model=TokenResponse)
async def login(
    data: Annotated[
        LoginUser, Body(description="Логин/пароль для авторизации пользователя")
    ],
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user_helper(data=data, session=session)
    token = create_access_token(data=data)
    return TokenResponse(access_token=token)
