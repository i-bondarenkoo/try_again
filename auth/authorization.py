from typing import Annotated
from fastapi import Depends, APIRouter, Body, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas.user import LoginUser, RegisterUser, ResponseUser
from auth.dependencies import register_helper, authenticate_user_helper
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from auth.jwt import create_access_token, decode_jwt
from schemas.token import TokenResponse
from db.settings import settings
import crud
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form")


@router.post("/register", response_model=ResponseUser)
async def register(
    data: Annotated[
        RegisterUser, Body(description="Данные пользователя для регистрации")
    ],
    session: AsyncSession = Depends(get_session),
):
    return await register_helper(data=data, session=session)


# @router.post("/login", response_model=TokenResponse)
# async def login(
#     data: Annotated[
#         LoginUser, Body(description="Логин/пароль для авторизации пользователя")
#     ],
#     session: AsyncSession = Depends(get_session),
# ):
#     user = await authenticate_user_helper(data=data, session=session)
#     token = create_access_token(user=user)
#     return TokenResponse(access_token=token)


@router.post("/login-form", response_model=TokenResponse)
async def login_with_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    # form_data.username и form_data.password
    data = LoginUser(login=form_data.username, password=form_data.password)
    user = await authenticate_user_helper(data=data, session=session)
    token = create_access_token(user=user)
    return TokenResponse(access_token=token)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
):
    decode_token: dict = decode_jwt(
        token=token, secret_key=settings.secret_key, algorithm=settings.algorithm
    )
    email = decode_token["email"]
    user = await crud.get_user_by_email(email=email, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
        )
    return user


@router.get("/me")
async def read_users(current_user: Annotated[ResponseUser, Depends(get_current_user)]):
    return ResponseUser(
        firstname=current_user.firstname,
        lastname=current_user.lastname,
        email=current_user.email,
        id=current_user.id,
    )
