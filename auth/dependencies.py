from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth.security import verify_password
from schemas.user import RegisterUser, LoginUser
import crud


async def register_helper(data: RegisterUser, session: AsyncSession):
    user = await crud.get_user_by_email(email=data.email, session=session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с такой почтой уже существует",
        )
    return await crud.create_user_crud(data, session)


async def authenticate_user_helper(data: LoginUser, session: AsyncSession):
    user = await crud.get_user_by_email(email=data.login, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверный логин"
        )
    check_password = verify_password(
        password=data.password, hashed_pwd=user.hashed_password
    )
    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверный пароль"
        )
    return user
