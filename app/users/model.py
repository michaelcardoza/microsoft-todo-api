from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from app.db.config import Base
from app.db.models import TimestampColums


class User(Base, TimestampColums):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)

    tasks = relationship("Task", back_populates="owner")
    task_groups = relationship("TaskGroup", back_populates="owner")

    def __init__(self, name, username, password):
        from app.auth.service import get_password_hash
        self.name = name
        self.username = username
        self.password = get_password_hash(password)
