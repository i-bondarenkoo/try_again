from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task import CreateTask
from models.task import TaskOrm


async def create_task_crud(task_in: CreateTask, session: AsyncSession):
    new_task = TaskOrm(**task_in.model_dump())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task
