import pytest
from common_lib.factories import UserModelFactory

from domains.update_action.models import UpdateActionRequestModel
from domains.update_action.services import UpdateActionService
from domains.users.factories import UserLoginCredentialsModelFactory
from domains.users.services import UserService
from use_cases.password_reset import password_reset_use_cases


@pytest.mark.asyncio
async def test_confirm_email_request_done(mocker, update_action_mock):
    # Создаем тестовые учетные данные для пользователя
    credentials = UserLoginCredentialsModelFactory.build()
    user = UserModelFactory.build()

    # Мокируем методы сервиса
    mocker.patch.object(UpdateActionService, "password_reset_create_action", return_value=update_action_mock)
    mocker.patch.object(UserService, "get_by_email", return_value=user)

    # Вызываем метод use case для запроса сброса пароля
    message, update_action = await password_reset_use_cases.password_reset_request(credentials=credentials)

    # Проверяем, что результат соответствует ожидаемому
    assert isinstance(update_action, UpdateActionRequestModel)
    assert isinstance(message, str)
    assert message == "create_action"


@pytest.mark.asyncio
async def test_confirm_email_request_no_user(mocker, update_action_mock):
    # Создаем тестовые учетные данные для пользователя
    credentials = UserLoginCredentialsModelFactory.build()

    # Мокируем методы сервиса
    mocker.patch.object(UpdateActionService, "password_reset_create_action", return_value=update_action_mock)
    mocker.patch.object(UserService, "get_by_email", return_value=None)

    # Вызываем метод use case для запроса сброса пароля
    message, update_action = await password_reset_use_cases.password_reset_request(credentials=credentials)

    # Проверяем, что результат соответствует ожидаемому
    assert isinstance(update_action, UpdateActionRequestModel)
    assert isinstance(message, str)
    assert message == "user_not_found"
