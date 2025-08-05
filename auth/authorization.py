from ast import stmt
from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from schemas.user import LoginUser, RegisterUser
from models.user import UserOrm
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from sqlalchemy import select
from fastapi import HTTPException, status
from auth.security import verify_password, hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register")
async def register(data: RegisterUser, session: AsyncSession = Depends(get_session)):
    stmt = select(UserOrm).where(UserOrm.email == data.login)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь уже зарегистрирован в системе",
        )
    hash_password = hash_password(current_password=data.password)
    user_db = UserOrm(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        hashed_password=hash_password(data.password),
    )
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)


# регистрация
# @router.post("/login")
# async def login(data: LoginUser, session: AsyncSession = Depends(get_session)):
#     stmt = select(UserOrm).where(UserOrm.email == data.login)
#     result = await session.execute(stmt)
#     user = result.scalars().first()
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Не верный логин или пароль"
#         )
#     hash_password = hash_password(current_password=data.password)
