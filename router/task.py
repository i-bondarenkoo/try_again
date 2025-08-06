from fastapi import APIRouter, Depends, Body, Path, HTTPException, status, Query
from models.task import TaskOrm
from schemas.task import CreateTask, ResponseTask, PathUpdateTask, ResponseTaskWithUser
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
import crud
from typing import Annotated
from crud.user import get_user_by_id_crud

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("/", response_model=ResponseTask)
async def create_task(
    task_in: Annotated[CreateTask, Body(description="Поля для создания объекта в БД")],
    session: AsyncSession = Depends(get_session),
):
    check_user = await get_user_by_id_crud(task_in.user_id, session)
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return await crud.create_task_crud(task_in=task_in, session=session)


@router.get("/{task_id}", response_model=ResponseTaskWithUser)
async def get_task_by_id(
    task_id: Annotated[
        int, Path(gt=0, description="ID задачи, для получения информации")
    ],
    session: AsyncSession = Depends(get_session),
):
    task = await crud.get_task_by_id_crud(task_id=task_id, session=session)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )
    return task


@router.get("/", response_model=list[ResponseTaskWithUser])
async def get_list_task(
    start: int = Query(0, ge=0, description="Начальный индекс списка задач"),
    stop: int = Query(3, gt=0, description="Конечный индекс списка задач"),
    session: AsyncSession = Depends(get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Начальный индекс списка не может быть больше конечного",
        )
    return await crud.get_list_task_crud(start=start, stop=stop, session=session)


@router.patch("/{task_id}", response_model=ResponseTask)
async def update_task(
    task_id: Annotated[int, Path(description="ID задачи для обновления")],
    task: Annotated[PathUpdateTask, Body(description="Данные для обновления")],
    session: AsyncSession = Depends(get_session),
):
    check_task = await session.get(TaskOrm, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    if task.user_id is not None:
        check_user = await get_user_by_id_crud(task.user_id, session)
        if not check_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )
    return await crud.update_task_crud(task=task, task_id=task_id, session=session)


@router.delete("/{task_id}")
async def delete_task(
    task_id: Annotated[int, Path(description="ID задачи для удаления")],
    session: AsyncSession = Depends(get_session),
):
    current_task = await crud.delete_task_crud(task_id, session)
    if current_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return current_task
