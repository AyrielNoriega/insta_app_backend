from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from core import database
from publications.router import publication_router
from users.router import user_router
from middlewares.error_handler import ErrorHandler
from users.schemas.token import Token
from users.schemas.user import User
from users.service import auth
from core.config import get_settings

settings = get_settings()

app = FastAPI()
app.title = "Insta Publications API"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)


database.Base.metadata.create_all(bind=database.engine)

app.include_router(publication_router)
app.include_router(user_router)


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(auth.get_current_active_user)]):
    return current_user


@app.post("/token")
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
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
