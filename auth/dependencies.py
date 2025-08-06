from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import RegisterUser
import crud


async def register_helper(data: RegisterUser, session: AsyncSession):
    user = await crud.get_user_by_email(email=data.email, session=session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует",
        )
    return await crud.create_user_crud(data, session)
