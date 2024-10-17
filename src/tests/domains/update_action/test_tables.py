import json
from datetime import datetime
from uuid import UUID

import pytest

from domains.update_action.tables import UpdateAction


@pytest.mark.asyncio
async def test_create_update_action(user_fixture):
    update_action = UpdateAction(user=user_fixture.id, pin_code="123456", update_data={"email_confirmed": True})
    await update_action.save()
    # Проверка, что запись создана
    assert update_action.id is not None
    assert isinstance(update_action.id, UUID)
    assert update_action.pin_code == "123456"
    assert update_action.update_data == {"email_confirmed": True}
    assert update_action.attempts == 3  # Значение по умолчанию
    assert isinstance(update_action.created_at, datetime)


@pytest.mark.asyncio
async def test_default_values(user_fixture):
    update_action = UpdateAction(user=user_fixture.id, pin_code="654321")
    await update_action.save()

    # Проверка значения по умолчанию для update_data и attempts
    assert json.loads(update_action.update_data) == {}, "update_data по умолчанию должно быть пустым словарем"
    assert update_action.attempts == 3


@pytest.mark.asyncio
async def test_foreign_key_cascade_delete(user_fixture):
    update_action = UpdateAction(user=user_fixture.id, pin_code="789123")
    await update_action.save()
    # Убедиться, что запись создана
    assert await UpdateAction.count() == 1
    # Удалить пользователя и проверить каскадное удаление
    await user_fixture.delete(force=True).run()
    # Запись должна быть удалена каскадно
    assert await UpdateAction.count() == 0
