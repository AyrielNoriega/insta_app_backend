from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, encode, decode
from datetime import datetime, timedelta, timezone
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from typing import Annotated

from users.schemas.token import TokenData
from users.schemas.user import User, UserInDB
from users.service.user import UserService
from utils.security import verify_password
from core import database
from core.config import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(username: str):
    db = database.Session()
    current_user = UserService(db).get_user_by_username(username)
    if current_user is None:
        return None
    user_dict = jsonable_encoder(current_user)
    user = UserInDB(**user_dict, hashed_password=user_dict["password"])
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def authenticate_user(
    username: str,
    password: str
):
    user = get_user(username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
