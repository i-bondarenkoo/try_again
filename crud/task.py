from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task import CreateTask, PathUpdateTask
from models.task import TaskOrm
from sqlalchemy import select
from fastapi import HTTPException, status


async def create_task_crud(task_in: CreateTask, session: AsyncSession):
    new_task = TaskOrm(**task_in.model_dump())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def get_task_by_id_crud(task_id: int, session: AsyncSession):
    task = await session.get(TaskOrm, task_id)
    return task


async def get_list_task_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = select(TaskOrm).order_by(TaskOrm.id).offset(start).limit(stop - start)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_task_crud(task_id: int, task: PathUpdateTask, session: AsyncSession):
    update_task = await session.get(TaskOrm, task_id)
    if not update_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    data: dict = task.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не переданы",
        )
    for k, v in data.items():
        if v is not None:
            setattr(update_task, k, v)
    await session.commit()
    await session.refresh(update_task)
    return update_task


async def delete_task_crud(task_id: int, session: AsyncSession):
    current_task = await session.get(TaskOrm, task_id)
    if not current_task:
        return None
    await session.delete(current_task)
    await session.commit()
    return {
        "message": "Задача удалена",
    }
