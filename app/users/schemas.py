from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
