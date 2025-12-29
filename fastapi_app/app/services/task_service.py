from __future__ import annotations

from app.repositories.task_repo import TaskRepository


class TaskService:
    def __init__(self, tasks: TaskRepository) -> None:
        self._tasks = tasks

    async def list_tasks(self, db, *, owner_id: int):
        return await self._tasks.list_for_owner(db, owner_id)

    async def create_task(self, db, *, owner_id: int, title: str, description: str | None):
        return await self._tasks.create(db, owner_id=owner_id, title=title, description=description)

    async def get_task(self, db, *, owner_id: int, task_id: int):
        task = await self._tasks.get_for_owner(db, owner_id, task_id)
        if not task:
            raise LookupError("task_not_found")
        return task

    async def update_task(self, db, *, owner_id: int, task_id: int, updates: dict):
        task = await self.get_task(db, owner_id=owner_id, task_id=task_id)
        for k, v in updates.items():
            if v is not None:
                setattr(task, k, v)
        return await self._tasks.update(db, task)

    async def delete_task(self, db, *, owner_id: int, task_id: int) -> None:
        task = await self.get_task(db, owner_id=owner_id, task_id=task_id)
        await self._tasks.delete(db, task)
