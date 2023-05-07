from typing import Annotated, Type

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.db.repository import BaseRepository, get_repository
from app.task_groups.model import TaskGroup
from app.task_groups.schemas import TaskGroupCreateSchema, TaskGroupUpdateSchema


class TaskGroupRepository(BaseRepository):
    def create(self, user_id: int, payload: TaskGroupCreateSchema) -> TaskGroup:
        new_task_group = TaskGroup(owner_id=user_id, **payload.dict())
        self.db.add(new_task_group)
        self.db.commit()
        self.db.refresh(new_task_group)
        return new_task_group

    def find(
        self,
        user_id: int,
        limit: int,
        page: int,
        order_by: list | None = None
    ) -> (int, list[Type[TaskGroup]]):
        query = self.db.query(TaskGroup)
        total = query.count()
        offset = (page - 1) * limit if page > 1 else 0

        if order_by is None:
            order_by = []

        query = query.filter_by(owner_id=user_id).order_by(*order_by)

        return total, query.limit(limit).offset(offset).all()

    def find_one(self, user_id: int, task_group_id: int):
        return self.db.query(TaskGroup).filter_by(id=task_group_id, owner_id=user_id).first()

    def update(self, task_group: TaskGroup, payload: TaskGroupUpdateSchema):
        update_data = payload.dict()
        for field in jsonable_encoder(task_group):
            if field in update_data:
                setattr(task_group, field, update_data[field])
        self.db.add(task_group)
        self.db.commit()
        self.db.refresh(task_group)
        return task_group

    def remove(self, task_group: TaskGroup):
        self.db.delete(task_group)
        self.db.commit()
        return task_group


TaskGroupRepositoryDep = Annotated[TaskGroupRepository, Depends(get_repository(TaskGroupRepository))]
