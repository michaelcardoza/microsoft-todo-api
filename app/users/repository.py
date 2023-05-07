from app.db.repository import BaseRepository
from app.users.model import User


class UserRepository(BaseRepository):
    def create(self, payload) -> User:
        new_user = User(**payload.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def find_one_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter_by(username=username).first()
