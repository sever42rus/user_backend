from common_lib.factories import UserModelFactory

from domains.users.exceptions import UniqueUserExceptions
from domains.users.models import TokenPairModel
from domains.users.services import temp_user_service


class TempUserUseCases:
    async def login_temp_user(self) -> TokenPairModel:
        """
        Логин временного пользователя. Генерация временного access-токена без refresh-токена.
        """
        user = UserModelFactory.build()
        if await temp_user_service.repository.exists(filter_params={"id": user.id}):
            raise UniqueUserExceptions()
        access_token_payload = temp_user_service.get_access_token_payload(user=user)
        access_token = temp_user_service.get_token(payload=access_token_payload.model_dump())
        return TokenPairModel(access=access_token, refresh=None)


temp_user_use_case = TempUserUseCases()
