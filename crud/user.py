from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserOrm
from schemas.user import CreateUser
from sqlalchemy import select


async def create_user_crud(user_in: CreateUser, session: AsyncSession):
    new_user = UserOrm(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_id_crud(user_id: int, session: AsyncSession):
    user = await session.get(UserOrm, user_id)
    return user


async def get_list_users_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = select(UserOrm).order_by(UserOrm.id).offset(start).limit(stop - start)
    result = await session.execute(stmt)
    return result.scalars().all()
