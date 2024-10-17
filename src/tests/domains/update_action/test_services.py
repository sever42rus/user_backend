from uuid import UUID

import pytest

from domains.update_action.models import UpdateActionModel
from domains.update_action.repository import PiccoloUpdateActionRepository
from domains.update_action.services import update_action_service


@pytest.mark.asyncio
async def test_email_confirm_create(mocker, update_action_mock):
    mocker.patch.object(PiccoloUpdateActionRepository, "create", return_value=update_action_mock)
    result = await update_action_service.email_confirm_create_action(user_id=update_action_mock.user)

    assert isinstance(result, UpdateActionModel)
    assert isinstance(result.id, UUID)
    assert result.id is not None


@pytest.mark.asyncio
async def test_get_by_id(mocker, update_action_mock):
    mocker.patch.object(PiccoloUpdateActionRepository, "get_by_fields", return_value=update_action_mock)
    result = await update_action_service.get_by_id(uuid=update_action_mock.id)

    assert isinstance(result, UpdateActionModel)
    assert isinstance(result.id, UUID)
    assert result.id == update_action_mock.id


@pytest.mark.asyncio
async def test_delete_by_id(mocker, update_action_mock):
    mocker.patch.object(PiccoloUpdateActionRepository, "delete", return_value=True)
    result = await update_action_service.delete_by_id(uuid=update_action_mock.id)

    assert result is True


@pytest.mark.asyncio
async def test_attempts_decrement_by_id(mocker, update_action_mock):
    mocker.patch.object(PiccoloUpdateActionRepository, "attempts_decrement", return_value=update_action_mock)
    result = await update_action_service.attempts_decrement_by_id(uuid=update_action_mock.id)

    assert isinstance(result, UpdateActionModel)
    assert isinstance(result.id, UUID)
    assert result.id == update_action_mock.id
    assert isinstance(result.attempts, int)
