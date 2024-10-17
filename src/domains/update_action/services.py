from uuid import UUID

from common_lib.models.users import UserModel

from domains.update_action.models import EmailConfirmModel
from domains.update_action.models import UpdateActionModel
from domains.update_action.repository import AbstractUpdateActionRepository
from domains.update_action.repository import PiccoloUpdateActionRepository
from domains.update_action.utils.pin_code import generate_pin_code
from domains.users.models import UserRegisterCredentialsModel


class UpdateActionService:
    def __init__(self, repository: AbstractUpdateActionRepository) -> None:
        self.repository: AbstractUpdateActionRepository = repository()

    async def email_confirm_create_action(self, user_id: UUID) -> UpdateActionModel:
        data = {"user": user_id, "pin_code": generate_pin_code(), "update_data": EmailConfirmModel().model_dump()}
        action_service = await self.repository.create(data=data)
        return action_service

    async def password_reset_create_action(
        self,
        user: UserModel,
        credentials: UserRegisterCredentialsModel,
    ) -> UpdateActionModel:
        data = {
            "user": user.id,
            "pin_code": generate_pin_code(),
            "update_data": credentials.model_dump(include=["password"]),
        }
        action_service = await self.repository.create(data=data)
        return action_service

    async def get_by_id(self, uuid: UUID) -> UpdateActionModel | None:
        return await self.repository.get_by_fields(filter_params={"id": uuid})

    async def delete_by_id(self, uuid: UUID) -> bool:
        return await self.repository.delete(filter_params={"id": uuid})

    async def attempts_decrement_by_id(self, uuid: UUID) -> UpdateActionModel | None:
        return await self.repository.attempts_decrement(filter_params={"id": uuid})


# Экземпляры сервисов пользователей и временных пользователей
update_action_service = UpdateActionService(repository=PiccoloUpdateActionRepository)
