from fastapi import HTTPException, status
from pydantic import BaseModel, root_validator


class AuthLoginSchema(BaseModel):
    username: str
    password: str

    @root_validator()
    def verify_fields(cls, values):
        if not values.get("username"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
        if not values.get("password"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")
        return values


class AuthRegisterSchema(AuthLoginSchema):
    name: str

    @root_validator()
    def verify_fields(cls, values):
        if not values.get("name"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required")
        return values


class AuthUserLoggedInSchema(BaseModel):
    name: str
    token: str = ""
