from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserOrm
from schemas.user import CreateUser, UpdateUser, RegisterUser
from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from auth.security import hash_password


async def create_user_crud(data: RegisterUser, session: AsyncSession):
    new_user = UserOrm(
        firstname=data.firstname,
        lastname=data.lastname,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_id_crud(user_id: int, session: AsyncSession):
    stmt = (
        select(UserOrm)
        .where(UserOrm.id == user_id)
        .options(selectinload(UserOrm.tasks))
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(email: str, session: AsyncSession):
    stmt = select(UserOrm).where(UserOrm.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_list_users_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = (
        select(UserOrm)
        .options(selectinload(UserOrm.tasks))
        .order_by(UserOrm.id)
        .offset(start)
        .limit(stop - start)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_user_crud(user_id: int, user: UpdateUser, session: AsyncSession):
    update_user = await get_user_by_id_crud(user_id, session)
    if not update_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    data: dict = user.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не переданы",
        )
    for k, v in data.items():
        if v is not None:
            setattr(update_user, k, v)
    await session.commit()
    await session.refresh(update_user)
    return update_user


async def delete_user_crud(user_id: int, session: AsyncSession):
    current_user = await session.get(UserOrm, user_id)
    if not current_user:
        return None
    await session.delete(current_user)
    await session.commit()
    return {
        "message": "Пользователь удален",
    }
