from typing import Annotated

from pydantic import AfterValidator
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from domains.users.utils.password import hash_password


class UserRegisterCredentialsModel(BaseModel):
    """
    Модель для регистрации пользователя. Включает email и пароль,
    где пароль будет захеширован с помощью валидатора AfterValidator.
    """

    email: EmailStr
    password: Annotated[str, AfterValidator(hash_password)]


class UserLoginCredentialsModel(BaseModel):
    """
    Модель для входа пользователя в систему. Включает email и пароль.
    """

    email: EmailStr
    password: str


class ChangePasswordModel(BaseModel):
    """
    Модель для изменения пароля. Включает старый пароль и новый, который также будет захеширован.
    Поле 'new_password' можно передавать под псевдонимом 'password' в запросе.
    """

    old_password: str
    new_password: Annotated[str, AfterValidator(hash_password)] = Field(alias="password")

    class Config:
        populate_by_name = True  # Разрешаем использовать оригинальные имена в запросе


class TokenPairModel(BaseModel):
    """
    Модель для пары токенов: access и refresh.
    Токен refresh может быть пустым (None).
    """

    access: str
    refresh: str | None
