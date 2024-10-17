from common_lib.models.users import AccessTokenPayloadModel

from domains.users.exceptions import UniqueUserExceptions
from domains.users.exceptions import UserLoginExceptions
from domains.users.models import ChangePasswordModel
from domains.users.models import TokenPairModel
from domains.users.models import UserLoginCredentialsModel
from domains.users.models import UserRegisterCredentialsModel
from domains.users.services import user_service
from domains.users.utils.password import verify_password


class UserUseCases:
    async def create(self, auth: AccessTokenPayloadModel, credentials: UserRegisterCredentialsModel) -> TokenPairModel:
        """
        Создание нового пользователя и генерация пары токенов (access и refresh).
        """
        exists_id = await user_service.exists_by_id(uuid=auth.id)
        exists_email = await user_service.exists_by_email(email=credentials.email)
        if exists_id or exists_email:
            raise UniqueUserExceptions()
        user = await user_service.create(
            data={
                **auth.model_dump(include=["id"]),
                **credentials.model_dump(),
            },
        )
        access_token_payload = user_service.get_access_token_payload(user=user)
        refresh_token_payload = user_service.get_refresh_token_payload(user=user)
        access_token = user_service.get_token(payload=access_token_payload.model_dump())
        refresh_token = user_service.get_token(payload=refresh_token_payload.model_dump())
        return TokenPairModel(access=access_token, refresh=refresh_token)

    async def login(self, credentials: UserLoginCredentialsModel) -> TokenPairModel:
        """
        Авторизация пользователя по email и паролю, и генерация пары токенов.
        """
        user = await user_service.get_by_email(email=credentials.email)
        if not user or not verify_password(user.password, credentials.password):
            raise UserLoginExceptions()
        access_token_payload = user_service.get_access_token_payload(user=user)
        refresh_token_payload = user_service.get_refresh_token_payload(user=user)
        access_token = user_service.get_token(payload=access_token_payload.model_dump())
        refresh_token = user_service.get_token(payload=refresh_token_payload.model_dump())
        return TokenPairModel(access=access_token, refresh=refresh_token)

    async def refresh(self, refresh_token: str) -> TokenPairModel:
        """
        Обновление access-токена с использованием refresh-токена.
        """
        refresh_token_payload = user_service.decode_refresh_token(refresh_token=refresh_token)
        user = await user_service.get_by_id(uuid=refresh_token_payload.id)
        if not user:
            # TODO: Добавить логику логирования случая, когда токен есть, а пользователя нет
            raise UserLoginExceptions()
        access_token_payload = user_service.get_access_token_payload(user=user)
        access_token = user_service.get_token(payload=access_token_payload.model_dump())
        return TokenPairModel(access=access_token, refresh=refresh_token)

    async def change_password(
        self,
        access_token_payload: AccessTokenPayloadModel,
        change_password: ChangePasswordModel,
    ) -> bool:
        """
        Смена пароля пользователя на основе access-токена и модели смены пароля.
        """
        user = await user_service.get_by_id(uuid=access_token_payload.id)
        if not user or not verify_password(user.password, change_password.old_password):
            raise UserLoginExceptions()
        return await user_service.update_by_id(
            uuid=access_token_payload.id,
            update_data=change_password.model_dump(include=["new_password"], by_alias=True),
        )


user_use_case = UserUseCases()
