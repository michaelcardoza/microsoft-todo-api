from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.config import get_db


class BaseRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @property
    def db(self) -> Session:
        return self._db


def get_repository(repository_type: Type[BaseRepository]):
    def _get_repository(db: Session = Depends(get_db)) -> BaseRepository:
        return repository_type(db)
    return _get_repository
