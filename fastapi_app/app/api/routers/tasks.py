from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session, get_current_user_id
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import TaskService
from app.repositories.task_repo import TaskRepository

router = APIRouter()


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
    db: AsyncSession = Depends(db_session),
    user_id: int = Depends(get_current_user_id),
) -> list[TaskOut]:
    svc = TaskService(TaskRepository())
    tasks = await svc.list_tasks(db, owner_id=user_id)
    return [TaskOut.model_validate(t) for t in tasks]


@router.post("/", response_model=TaskOut, status_code=201)
async def create_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(db_session),
    user_id: int = Depends(get_current_user_id),
) -> TaskOut:
    svc = TaskService(TaskRepository())
    task = await svc.create_task(db, owner_id=user_id, title=payload.title, description=payload.description)
    return TaskOut.model_validate(task)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(db_session),
    user_id: int = Depends(get_current_user_id),
) -> TaskOut:
    svc = TaskService(TaskRepository())
    task = await svc.get_task(db, owner_id=user_id, task_id=task_id)
    return TaskOut.model_validate(task)


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: AsyncSession = Depends(db_session),
    user_id: int = Depends(get_current_user_id),
) -> TaskOut:
    svc = TaskService(TaskRepository())
    updates = payload.model_dump(exclude_unset=True)
    task = await svc.update_task(db, owner_id=user_id, task_id=task_id, updates=updates)
    return TaskOut.model_validate(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(db_session),
    user_id: int = Depends(get_current_user_id),
) -> Response:
    svc = TaskService(TaskRepository())
    await svc.delete_task(db, owner_id=user_id, task_id=task_id)
    return Response(status_code=204)
