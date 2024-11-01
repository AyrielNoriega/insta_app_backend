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
