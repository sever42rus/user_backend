from typing import Tuple

from domains.update_action.factories import UpdateActionRequestModelFactory
from domains.update_action.models import UpdateActionRequestModel
from domains.update_action.services import update_action_service
from domains.users.models import UserRegisterCredentialsModel
from domains.users.services import user_service


class PasswordResetUseCases:
    async def password_reset_request(
        self,
        credentials: UserRegisterCredentialsModel,
    ) -> Tuple[str, UpdateActionRequestModel]:
        user = await user_service.get_by_email(email=credentials.email)
        if user is None:
            return "user_not_found", UpdateActionRequestModelFactory.build()
        update_action = await update_action_service.password_reset_create_action(user=user, credentials=credentials)

        # TODO Тут нужна реализауия отправки пин когда в сервис отправки
        print(update_action.pin_code)

        return "create_action", UpdateActionRequestModel(**update_action.model_dump())


password_reset_use_cases = PasswordResetUseCases()
