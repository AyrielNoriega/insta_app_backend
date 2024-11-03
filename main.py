from fastapi import Depends, FastAPI

from core import database
from publications.router import publication_router
from users.router.users import user_router
from users.router.auth import auth_router
from middlewares.error_handler import ErrorHandler
from core.config import get_settings

settings = get_settings()

app = FastAPI(
    openapi_prefix=settings.API_VERSION,
)
app.title = settings.APP_NAME
app.version = "1.0.0"
app.add_middleware(ErrorHandler)


database.Base.metadata.create_all(bind=database.engine)

app.include_router(publication_router)
app.include_router(user_router)
app.include_router(auth_router)
