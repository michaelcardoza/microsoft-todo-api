from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.shared.resources import strings
from app.db.repository import get_repository
from app.auth.schemas import AuthLoginSchema, AuthRegisterSchema, AuthUserLoggedInSchema
from app.auth.service import verify_password, create_access_token
from app.users.repository import UserRepository
from app.users.schemas import UserSchema

router = APIRouter()
UserRepositoryDep = Annotated[UserRepository, Depends(get_repository(UserRepository))]


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthUserLoggedInSchema)
def login(payload: AuthLoginSchema, user_repository: UserRepositoryDep):
    user = user_repository.find_one_by_username(payload.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_DOES_NOT_EXIST_ERROR)
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strings.AUTH_LOGIN_ERROR)
    token = create_access_token({
        "sub": user.username
    })
    return {
        "name": user.name,
        "token": token
    }


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
def register(payload: AuthRegisterSchema, user_repository: UserRepositoryDep):
    user = user_repository.create(payload)
    return user
