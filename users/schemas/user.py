from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=3, max_length=255)
    username: str = Field(..., min_length=3, max_length=255)
    email: str = Field(..., min_length=3, max_length=255)
    disabled: bool = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "ayriel noriega",
                    "email": "ayriel@gmail.com",
                    "username": "ayriel",
                }
            ]
        }
    }


class UserRegister(User):
    # name: str = Field(..., min_length=3, max_length=255)
    # username: str = Field(..., min_length=3, max_length=255)
    # email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=3, max_length=255)


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "ayriel noriega",
                    "username": "ayriel",
                    "email": "ayriel@gmail.com",
                    "password": "123456"
                }
            ]
        }
    }


class UserInDB(User):
    hashed_password: str
