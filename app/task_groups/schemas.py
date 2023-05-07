from datetime import datetime

from pydantic import BaseModel


class TaskGroupBaseSchema(BaseModel):
    name: str


class TaskGroupSchema(TaskGroupBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskGroupListSchema(BaseModel):
    data: list[TaskGroupSchema]
    total: int
    has_more: bool


class TaskGroupCreateSchema(TaskGroupBaseSchema):
    pass


class TaskGroupUpdateSchema(TaskGroupBaseSchema):
    pass
