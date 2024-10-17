from uuid import uuid4

import pytest

from core.exceptions import MultipleObjectsException
from domains.update_action.repository import PiccoloUpdateActionRepository


@pytest.mark.asyncio
async def test_create(user_fixture):
    repo = PiccoloUpdateActionRepository()
    data = {"user": user_fixture.id, "pin_code": "123456", "update_data": {"email_confirmed": True}}

    action = await repo.create(data)
    assert action.user == data["user"]
    assert action.pin_code == data["pin_code"]
    assert action.update_data == data["update_data"]


@pytest.mark.asyncio
async def test_get_by_fields_multiple_error(user_fixture):
    repo = PiccoloUpdateActionRepository()
    data = {"user": user_fixture.id, "pin_code": "123456", "update_data": {"email_confirmed": True}}

    await repo.create(data)
    await repo.create(data)
    with pytest.raises(MultipleObjectsException):
        await repo.get_by_fields({"user": user_fixture.id})


@pytest.mark.asyncio
async def test_get_by_fields(update_action_fixture):
    repo = PiccoloUpdateActionRepository()
    found_action = await repo.get_by_fields({"id": update_action_fixture.id})

    assert found_action is not None
    assert found_action.user == update_action_fixture["user"]
    assert found_action.pin_code == update_action_fixture["pin_code"]
    assert found_action.update_data == update_action_fixture["update_data"]


@pytest.mark.asyncio
async def test_exists(update_action_fixture):
    repo = PiccoloUpdateActionRepository()
    exists = await repo.exists({"id": update_action_fixture.id})

    assert exists is True
    exists = await repo.exists({"user": uuid4()})
    assert exists is False


@pytest.mark.asyncio
async def test_update(update_action_fixture):
    repo = PiccoloUpdateActionRepository()
    filter_params = {"id": update_action_fixture.id}
    update_data = {"pin_code": "654321"}
    updated = await repo.update(filter_params, update_data)

    assert updated is True
    updated_action = await repo.get_by_fields(filter_params)
    assert updated_action.pin_code == update_data["pin_code"]


@pytest.mark.asyncio
async def test_attempts_decrement(update_action_fixture):
    repo = PiccoloUpdateActionRepository()
    updated = await repo.attempts_decrement(filter_params={"id": update_action_fixture.id})
    found_action = await repo.get_by_fields({"id": update_action_fixture.id})

    assert updated.attempts == found_action.attempts


@pytest.mark.asyncio
async def test_delete(update_action_fixture):
    repo = PiccoloUpdateActionRepository()

    assert await repo.exists(filter_params={"id": update_action_fixture.id}) is True
    result = await repo.delete(filter_params={"id": update_action_fixture.id})
    assert result is True
    assert await repo.exists(filter_params={"id": update_action_fixture.id}) is False
