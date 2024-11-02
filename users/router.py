
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from config.database import Session
from users.schemas.user import User, UserRegister
from users.service import UserService

user_router = APIRouter()
user_router.prefix = "/users"



@user_router.post('/register', tags=["users"], status_code=201, response_model=dict)
def register(user: UserRegister):
    db = Session()
    existing_user = UserService(db).get_user_by_email(user.email)
    print("existing_user", not existing_user)
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


@user_router.put('/{id}', tags=["users"], status_code=200, response_model=dict)
def update_user(id: int, user: User):
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
