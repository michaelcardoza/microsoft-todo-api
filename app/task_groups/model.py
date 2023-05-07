from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.config import Base
from app.db.models import TimestampColums


class TaskGroup(Base, TimestampColums):
    __tablename__ = "task_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="task_groups")
    tasks = relationship("Task", back_populates="task_group")

    def __init__(self, owner_id: int, name: str):
        self.owner_id = owner_id
        self.name = name
