from fastapi import APIRouter, Depends
from schemas.task import CreateTask, ResponseTask
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
import crud

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("/", response_model=ResponseTask)
async def create_task(
    task_in: CreateTask, session: AsyncSession = Depends(get_session)
):
    return await crud.create_task_crud(task_in=task_in, session=session)
