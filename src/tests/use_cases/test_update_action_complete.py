import pytest
from common_lib.factories import AccessTokenPayloadModelFactory

from core.exceptions import BadRequestException
from domains.update_action.factories import UpdateActionModelFactory
from domains.update_action.services import UpdateActionService
from domains.users.services import UserService
from use_cases.update_action_complete import update_action_use_case


@pytest.mark.asyncio
async def test_confirm_email_complete_not_found_record(mocker):
    # Создаем тестовый объект аутентификации (auth)
    auth = AccessTokenPayloadModelFactory.build()
    # Создаем тестовое действие обновления
    update_action = UpdateActionModelFactory().build(user=auth.id)

    # Мокируем метод получения действия по ID, чтобы вернуть None
    mocker.patch.object(UpdateActionService, "get_by_id", return_value=None)

    # Проверяем, что вызывается исключение BadRequestException, если запись не найдена
    with pytest.raises(BadRequestException, match="is_none"):
        await update_action_use_case.verify_and_complete(update_action_data=update_action)


@pytest.mark.asyncio
async def test_confirm_email_complete_wrong_pin_code_decrement(mocker):
    # Создаем тестовый объект аутентификации (auth)
    auth = AccessTokenPayloadModelFactory.build()
    # Создаем тестовое действие обновления
    update_action = UpdateActionModelFactory().build(user=auth.id)
    update_action_decremented = update_action
    update_action_decremented.attempts -= 1  # Уменьшаем количество попыток

    # Мокируем метод получения действия по ID
    mocker.patch.object(UpdateActionService, "get_by_id", return_value=update_action)
    # Мокируем метод уменьшения попыток
    mocker.patch.object(UpdateActionService, "attempts_decrement_by_id", return_value=update_action_decremented)

    # Создаем новое действие с неправильным PIN-кодом
    update_action = UpdateActionModelFactory().build(user=auth.id, pin_code="654321")
    # Проверяем, что вызывается исключение BadRequestException при неверном PIN-коде
    with pytest.raises(BadRequestException, match=f"wrong_pin_code_attempts_{update_action_decremented.attempts}"):
        await update_action_use_case.verify_and_complete(update_action_data=update_action)


@pytest.mark.asyncio
async def test_confirm_email_complete_wrong_pin_code_delete(mocker):
    # Создаем тестовый объект аутентификации (auth)
    auth = AccessTokenPayloadModelFactory.build()
    # Создаем тестовое действие обновления с одной попыткой
    update_action = UpdateActionModelFactory().build(user=auth.id, attempts=1)
    update_action_decremented = update_action
    update_action_decremented.attempts -= 1  # Уменьшаем количество попыток

    # Мокируем метод получения действия по ID
    mocker.patch.object(UpdateActionService, "get_by_id", return_value=update_action)
    # Мокируем метод удаления действия по ID
    mocker.patch.object(UpdateActionService, "delete_by_id", return_value=True)

    # Создаем новое действие с неправильным PIN-кодом
    update_action = UpdateActionModelFactory().build(user=auth.id, pin_code="654321")
    # Проверяем, что вызывается исключение BadRequestException при неверном PIN-коде
    with pytest.raises(BadRequestException, match="wrong_pin_code_attempts_0"):
        await update_action_use_case.verify_and_complete(update_action_data=update_action)


@pytest.mark.asyncio
async def test_confirm_email_complete_done(mocker, user_model_mock):
    # Создаем тестовый объект аутентификации (auth)
    auth = AccessTokenPayloadModelFactory.build()
    # Создаем тестовое действие обновления с одной попыткой
    update_action = UpdateActionModelFactory().build(user=auth.id, attempts=1)

    # Мокируем метод получения действия по ID
    mocker.patch.object(UpdateActionService, "get_by_id", return_value=update_action)
    # Мокируем метод удаления действия по ID
    mocker.patch.object(UpdateActionService, "delete_by_id", return_value=True)
    # Мокируем метод обновления пользователя по ID
    mocker.patch.object(UserService, "update_by_id", return_value=user_model_mock)

    # Вызываем метод проверки и завершения действия обновления
    result = await update_action_use_case.verify_and_complete(update_action_data=update_action)
    # Проверяем, что результат соответствует ожидаемому
    assert result is True
