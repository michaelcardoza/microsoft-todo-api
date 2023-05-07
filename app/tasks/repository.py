from typing import Annotated, List, Type

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.db.repository import BaseRepository, get_repository
from app.tasks.model import Task
from app.tasks.schemas import TaskCreateSchema, TaskUpdateSchema


class TaskRepository(BaseRepository):
    def create(self, user_id: int, payload: TaskCreateSchema) -> Task:
        new_task = Task(owner_id=user_id, **payload.dict())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def find(
        self,
        user_id: int,
        limit: int,
        page: int,
        group: int = None,
        order_by: list | None = None
    ) -> (int, list[Type[Task]]):
        query = self.db.query(Task)
        total = query.count()
        offset = (page - 1) * limit if page > 1 else 0

        if order_by is None:
            order_by = []

        if group is not None:
            query = query.filter_by(owner_id=user_id, task_group_id=group).order_by(*order_by)
        else:
            query = query.filter_by(owner_id=user_id).order_by(*order_by)

        return total, query.limit(limit).offset(offset).all()

    def find_one(self, user_id: int, task_id: int):
        return self.db.query(Task).filter_by(id=task_id, owner_id=user_id).first()

    def update(self, task: Task, payload: TaskUpdateSchema):
        update_data = payload.dict()
        for field in jsonable_encoder(task):
            if field in update_data:
                setattr(task, field, update_data[field])
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def remove(self, task: Task):
        self.db.delete(task)
        self.db.commit()
        return task


TaskRepositoryDep = Annotated[TaskRepository, Depends(get_repository(TaskRepository))]
