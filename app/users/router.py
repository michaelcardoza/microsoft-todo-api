from fastapi import APIRouter, status

from app.shared.depends import UserLoggedInDep
from app.users.schemas import UserSchema

router = APIRouter()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema)
def get_logged_in_user(current_user: UserLoggedInDep):
    return current_user
