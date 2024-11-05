from pydantic import BaseModel, Field


class Publication(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=3)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My first publication",
                    "content": "This is the content of my first publication"
                }
            ]
        }
    }


class PublicationInDb(Publication):
    id: int
    user_id: int
    created_at: str
    updated_at: str


class PublicationResponse(Publication):
    id: int
    author: str
    created_at: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "My first publication",
                    "content": "This is the content of my first publication",
                    "created_at": "2021-10-20T00:00:00",
                    "author": "Ayriel Noriega"
                }
            ]
        }
    }
