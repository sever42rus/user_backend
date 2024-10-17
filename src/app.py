from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from auth_lib import exceptions as auth_lib_exceptions
from fastapi import FastAPI
from jwt import exceptions as jwt_exceptions
from piccolo.engine import engine_finder

from api import exception_handlers
from api.handlers import router
from core import exceptions as core_exceptions
from domains.users import exceptions as user_exceptions
from settings import fastapi_settings
from utils import get_project_version


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    engine = engine_finder()
    await engine.start_connection_pool(min_size=0, max_size=10, max_inactive_connection_lifetime=5)
    yield
    await engine.close_connection_pool()


app = FastAPI(
    title="user-backend-open-api",
    version=get_project_version(),
    lifespan=lifespan,
    **fastapi_settings.model_dump(),
)

app.include_router(router, prefix="/api/v1/user")


app.add_exception_handler(user_exceptions.UniqueUserExceptions, exception_handlers.email_is_not_unique)
app.add_exception_handler(user_exceptions.UserLoginExceptions, exception_handlers.incorrect_login_or_password)
app.add_exception_handler(auth_lib_exceptions.NotAuthorizedExceptions, exception_handlers.not_authorized)
app.add_exception_handler(jwt_exceptions.DecodeError, exception_handlers.token_decode)
app.add_exception_handler(jwt_exceptions.ExpiredSignatureError, exception_handlers.token_expired_signature)
app.add_exception_handler(auth_lib_exceptions.AccessDeniedExceptions, exception_handlers.access_denied)
app.add_exception_handler(core_exceptions.BadRequestException, exception_handlers.bad_request)
