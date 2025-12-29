from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    async def list_for_owner(self, db: AsyncSession, owner_id: int) -> list[Task]:
        res = await db.execute(select(Task).where(Task.owner_id == owner_id).order_by(Task.id.desc()))
        return list(res.scalars().all())

    async def get_for_owner(self, db: AsyncSession, owner_id: int, task_id: int) -> Task | None:
        res = await db.execute(select(Task).where(Task.owner_id == owner_id, Task.id == task_id))
        return res.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, owner_id: int, title: str, description: str | None) -> Task:
        task = Task(owner_id=owner_id, title=title, description=description)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    async def update(self, db: AsyncSession, task: Task) -> Task:
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    async def delete(self, db: AsyncSession, task: Task) -> None:
        await db.delete(task)
        await db.commit()
