from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import Dict
from uuid import UUID

import jwt
from common_lib.models.choices import BaseAccessLevelModel
from common_lib.models.users import AccessTokenPayloadModel
from common_lib.models.users import RefreshTokenPayloadModel
from common_lib.models.users import UserModel

from domains.users.repositories import AbstractUserRepository
from domains.users.repositories import PiccoloUserRepository
from settings import jwt_settings


class UserService:
    """
    Сервис для управления пользователями: регистрация, авторизация, смена пароля и работа с токенами.
    """

    def __init__(self, repository: AbstractUserRepository) -> None:
        """
        Инициализация сервиса с использованием репозитория пользователей.
        """
        self.repository: AbstractUserRepository = repository()

    def get_access_token_payload(self, user: UserModel) -> AccessTokenPayloadModel:
        """
        Формирование полезной нагрузки для access-токена, основываясь на уровне доступа пользователя.
        """
        regular_access = BaseAccessLevelModel.regular.value
        not_confirmed_access = BaseAccessLevelModel.not_confirmed.value
        return AccessTokenPayloadModel(
            exp=datetime.now(tz=timezone.utc) + timedelta(hours=jwt_settings.access_token_exp),
            id=str(user.id),
            access_level=(user.access_level or regular_access if user.email_confirmed else not_confirmed_access),
            # Дополнительные данные могут быть добавлены сюда
        )

    def get_refresh_token_payload(self, user: UserModel) -> RefreshTokenPayloadModel:
        """
        Формирование полезной нагрузки для refresh-токена.
        """
        return RefreshTokenPayloadModel(
            exp=datetime.now(tz=timezone.utc) + timedelta(days=jwt_settings.refresh_token_exp),
            id=str(user.id),
            # Дополнительные данные могут быть добавлены сюда
        )

    def decode_refresh_token(self, refresh_token: str) -> RefreshTokenPayloadModel:
        """
        Декодирование refresh-токена и возврат полезной нагрузки.
        """
        payload = jwt.decode(refresh_token, jwt_settings.public_key, algorithms=["RS256"])
        return RefreshTokenPayloadModel(**payload)

    def get_token(self, payload: Dict[str, Any]) -> str:
        """
        Кодирование полезной нагрузки в JWT-токен.
        """
        return jwt.encode(payload, jwt_settings.private_key, algorithm="RS256")

    async def create(self, data: Dict[str, Any]) -> UserModel:
        return await self.repository.create(data=data)

    async def update_by_id(self, uuid: UUID, update_data=Dict[str, Any]) -> bool:
        return await self.repository.update(filter_params={"id": uuid}, update_data=update_data)

    async def get_by_id(self, uuid: UUID) -> UserModel | None:
        return await self.repository.get_by_fields(filter_params={"id": uuid})

    async def get_by_email(self, email: str) -> UserModel | None:
        return await self.repository.get_by_fields(filter_params={"email": email})

    async def exists_by_id(self, uuid: UUID) -> bool:
        return await self.repository.exists(filter_params={"id": uuid})

    async def exists_by_email(self, email: str) -> bool:
        return await self.repository.exists(filter_params={"email": email})


class TempUserService(UserService):
    """
    Сервис для временных пользователей. Наследуется от основного сервиса пользователей.
    """

    def get_access_token_payload(self, user: UserModel) -> AccessTokenPayloadModel:
        """
        Формирование полезной нагрузки для временного access-токена, который действует 7 дней.
        """
        return AccessTokenPayloadModel(
            exp=datetime.now(tz=timezone.utc) + timedelta(days=7),
            id=user.id,
            access_level=BaseAccessLevelModel.temp.value,
            # Дополнительные данные могут быть добавлены сюда
        )


# Экземпляры сервисов пользователей и временных пользователей
user_service = UserService(repository=PiccoloUserRepository)
temp_user_service = TempUserService(repository=PiccoloUserRepository)
