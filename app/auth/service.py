from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.shared.resources import strings
from app.core.config import get_settings
from app.db.repository import get_repository
from app.users.repository import UserRepository

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(payload: dict):
    expire = datetime.utcnow() + timedelta(days=int(settings.jwt_expiration_days))
    claims = {
        "exp": expire,
        **payload
    }
    encoded_jwt = jwt.encode(claims, settings.jwt_secret, algorithm="HS256")
    return encoded_jwt


def get_logged_in_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: Annotated[UserRepository, Depends(get_repository(UserRepository))]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=strings.AUTH_TOKEN_ERROR
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = user_repository.find_one_by_username(username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
