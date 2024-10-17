import pytest
from common_lib.factories import AccessTokenPayloadModelFactory

from domains.update_action.models import UpdateActionRequestModel
from domains.update_action.services import UpdateActionService
from use_cases.confirm_email import confirm_email_use_cases


@pytest.mark.asyncio
async def test_confirm_email_request(mocker, update_action_mock):
    # Создаем тестовый объект аутентификации (auth)
    auth = AccessTokenPayloadModelFactory.build()

    # Мокируем метод сервиса для создания действия подтверждения email
    mocker.patch.object(UpdateActionService, "email_confirm_create_action", return_value=update_action_mock)

    # Вызываем метод use case для запроса подтверждения email
    result = await confirm_email_use_cases.confirm_email_request(auth)

    # Проверяем, что результат соответствует ожидаемому
    assert isinstance(result, UpdateActionRequestModel)
    assert result.id == update_action_mock.id
