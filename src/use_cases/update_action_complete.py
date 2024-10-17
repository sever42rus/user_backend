from core.exceptions import BadRequestException
from domains.update_action.models import UpdateActionCompleteModel
from domains.update_action.services import update_action_service
from domains.users.services import user_service


class UpdateActionUseCase:
    async def verify_and_complete(
        self,
        update_action_data: UpdateActionCompleteModel,
    ) -> bool:
        # Получаем действие по ID
        update_action = await update_action_service.get_by_id(uuid=update_action_data.id)
        if update_action is None:
            raise BadRequestException("is_none", message="Не удалось подтвердить email")
        # Проверка корректности пин-кода
        if update_action.pin_code != update_action_data.pin_code:
            # Если попытки исчерпаны — удаляем запись
            if update_action.attempts <= 1:
                await update_action_service.delete_by_id(uuid=update_action.id)
            else:
                # Иначе уменьшаем количество попыток
                await update_action_service.attempts_decrement_by_id(uuid=update_action.id)
            raise BadRequestException(
                f"wrong_pin_code_attempts_{update_action.attempts}",
                message="Не удалось подтвердить email",
            )

        # Обновляем пользователя
        await user_service.update_by_id(uuid=update_action.user, update_data=update_action.update_data)
        await update_action_service.delete_by_id(uuid=update_action.id)
        # Возвращаем успешный результат
        return True


update_action_use_case = UpdateActionUseCase()
