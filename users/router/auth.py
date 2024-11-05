from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

from users.schemas.token import Token
from users.service import auth
from users.schemas.user import User
from core.security import create_access_token
from core.config import get_settings

settings = get_settings()


auth_router = APIRouter()
# auth_router.prefix = "/auth"
auth_router.tags = ["auth"]


# @auth_router.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(auth.get_current_active_user)]):
#     return current_user


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name
        },
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")
