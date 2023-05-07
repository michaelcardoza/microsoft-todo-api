from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column

from app.db.config import Base
from app.db.models import TimestampColums


class Task(Base, TimestampColums):
    __tablename__ = "tasks"

    id = mapped_column(Integer, primary_key=True, index=True)
    content = mapped_column(String, nullable=False)
    is_complete = mapped_column(Boolean, nullable=False, default=False)
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    task_group_id = mapped_column(Integer, ForeignKey("task_groups.id"), nullable=True)

    owner = relationship("User", back_populates="tasks")
    task_group = relationship("TaskGroup", back_populates="tasks")

    def __init__(self, content: str, owner_id: int, task_group_id: int | None = None):
        self.content = content
        self.owner_id = owner_id
        if task_group_id is not None:
            self.task_group_id = task_group_id

    def to_dict(self):
        print(self.__table__.columns)
