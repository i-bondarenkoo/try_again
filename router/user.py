from fastapi import APIRouter, Body, Query, Path, Depends, HTTPException, status
import crud
from db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import (
    CreateUser,
    ResponseUser,
    UpdateUser,
    ResponseUserWithRelationship,
)
from typing import Annotated


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=ResponseUser)
async def create_user(
    user_in: Annotated[CreateUser, Body(description="Данные пользователя")],
    session: AsyncSession = Depends(get_session),
):
    return await crud.create_user_crud(user_in=user_in, session=session)


@router.get("/{user_id}", response_model=ResponseUserWithRelationship)
async def get_user_by_id(
    user_id: Annotated[
        int, Path(gt=0, description="ID пользователя для просмотра данных")
    ],
    session: AsyncSession = Depends(get_session),
):
    result = await crud.get_user_by_id_crud(user_id=user_id, session=session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return result


@router.get("/", response_model=list[ResponseUserWithRelationship])
async def get_list_users(
    start: int = Query(0, ge=0, description="Начальный индекс списка пользователей"),
    stop: int = Query(3, gt=0, description="Конечный индекс списка пользователей"),
    session: AsyncSession = Depends(get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Начальный индекс списка не может быть больше конечного",
        )
    return await crud.get_list_users_crud(start=start, stop=stop, session=session)


@router.patch("/{user_id}", response_model=ResponseUser)
async def update_user(
    user_id: Annotated[int, Path(description="ID пользователя для обновления")],
    user: Annotated[UpdateUser, Body(description="Данные для обновления")],
    session: AsyncSession = Depends(get_session),
):
    return await crud.update_user_crud(
        user_id=user_id,
        user=user,
        session=session,
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(description="ID пользователя для удаления")],
    session: AsyncSession = Depends(get_session),
):
    result = await crud.delete_user_crud(user_id, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return result
