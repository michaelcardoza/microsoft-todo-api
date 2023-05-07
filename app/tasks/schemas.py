from datetime import datetime

from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    content: str
    task_group_id: int | None = None


class TaskSchema(TaskBaseSchema):
    id: int
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskListSchema(BaseModel):
    data: list[TaskSchema]
    total: int
    has_more: bool


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass
