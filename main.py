from fastapi import FastAPI

from config.database import engine, Base
from publications.router import publication_router
from users.router import user_router
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "Insta Publications API"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)


app.include_router(publication_router)
app.include_router(user_router)