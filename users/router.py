
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from core.database import Session
from users.schemas.user import User, UserRegister
from users.service.user import UserService

user_router = APIRouter()
user_router.prefix = "/users"
user_router.tags = ["users"]



@user_router.post('/register', status_code=201, response_model=dict)
async def register(user: UserRegister):
    db = Session()
    existing_user = UserService(db).get_user_by_email(user.email)

    if not existing_user:
        UserService(db).register(user)
        status_code=201
        content="User created successfully"
    else:
        status_code=400
        content="User already exists"

    return JSONResponse(
        status_code=status_code,
        content=content
    )


@user_router.put('/{id}', status_code=200, response_model=dict)
async def update_user(id: int, user: User):
    db = Session()
    result = UserService(db).get_user_by_id(id)
    if not result:
        content = {"message": "User not found"}
        status = 404
    else:
        UserService(db).update_user(id, user)
        content = "User updated successfully"
        status = 200

    return JSONResponse(
        status_code=status,
        content=content
    )
