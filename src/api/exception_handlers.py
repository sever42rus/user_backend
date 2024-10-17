from auth_lib.exceptions import AccessDeniedExceptions
from auth_lib.exceptions import NotAuthorizedExceptions
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from jwt.exceptions import DecodeError
from jwt.exceptions import ExpiredSignatureError

from core.exceptions import BadRequestException
from domains.users.exceptions import UniqueUserExceptions
from domains.users.exceptions import UserLoginExceptions


async def email_is_not_unique(request: Request, exc: UniqueUserExceptions):
    """
    Возвращает ответ с кодом 400, если email пользователя уже существует.
    """
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Пользователь уже существует"})


async def incorrect_login_or_password(request: Request, exc: UserLoginExceptions):
    """
    Возвращает ответ с кодом 400, если введены неверные логин или пароль.
    """
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Неверный логин или пароль"})


async def token_decode(request: Request, exc: DecodeError):
    """
    Возвращает ответ с кодом 400, если токен не может быть декодирован.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Плохой токен, невозможно обработать =("},
    )


async def token_expired_signature(request: Request, exc: ExpiredSignatureError):
    """
    Возвращает ответ с кодом 400, если срок действия токена истек.
    """
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Время жизни токена истекло"})


async def not_authorized(request: Request, exc: NotAuthorizedExceptions):
    """
    Возвращает ответ с кодом 401, если пользователь не авторизован.
    """
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Не авторизован"})


async def access_denied(request: Request, exc: AccessDeniedExceptions):
    """
    Возвращает ответ с кодом 403, если у пользователя нет прав для выполнения действия.
    """
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Нет прав для действия"})


async def bad_request(request: Request, exc: BadRequestException):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc.message)})
