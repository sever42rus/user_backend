from common_lib.models.users import AccessTokenPayloadModel

from domains.update_action.models import UpdateActionRequestModel
from domains.update_action.services import update_action_service


class ConfirmEmailUseCases:
    async def confirm_email_request(self, auth: AccessTokenPayloadModel) -> UpdateActionRequestModel:
        update_action = await update_action_service.email_confirm_create_action(user_id=auth.id)

        # TODO Тут нужна реализауия отправки пин когда в сервис отправки
        print(update_action.pin_code)

        return UpdateActionRequestModel(**update_action.model_dump())


confirm_email_use_cases = ConfirmEmailUseCases()
