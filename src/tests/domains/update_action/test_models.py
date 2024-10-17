from datetime import datetime
from uuid import UUID
from uuid import uuid4

import pytest
from pydantic import ValidationError

from domains.update_action.models import EmailConfirmModel
from domains.update_action.models import UpdateActionCompleteModel
from domains.update_action.models import UpdateActionModel
from domains.update_action.models import UpdateActionRequestModel


def test_email_confirm_model_default_value():
    model = EmailConfirmModel()
    assert model.email_confirmed is True


def test_update_action_request_model_valid():
    model = UpdateActionRequestModel(id=uuid4())
    assert isinstance(model.id, UUID)


def test_update_action_complete_model_valid():
    model = UpdateActionCompleteModel(id=uuid4(), pin_code="123456")
    assert isinstance(model.id, UUID)
    assert model.pin_code == "123456"


def test_update_action_complete_model_invalid_pin_code_length():
    with pytest.raises(ValidationError):
        UpdateActionCompleteModel(id=uuid4(), pin_code="12345")  # Too short

    with pytest.raises(ValidationError):
        UpdateActionCompleteModel(id=uuid4(), pin_code="1234567")  # Too long

    with pytest.raises(ValidationError, match="PIN code must contain only digits"):
        UpdateActionCompleteModel(id=uuid4(), pin_code="qwerty")  # Too long


def test_update_action_model_valid():
    model = UpdateActionModel(
        id=uuid4(),
        user=uuid4(),
        pin_code="123456",
        update_data='{"key": "value"}',  # valid JSON string
        attempts=3,
        created_at=datetime.now(),
    )
    assert isinstance(model.id, UUID)
    assert model.pin_code == "123456"
    assert model.update_data == {"key": "value"}  # check if JSON loads correctly
    assert model.attempts == 3
    assert isinstance(model.created_at, datetime)


def test_update_action_model_invalid_pin_code():
    with pytest.raises(ValidationError):
        UpdateActionModel(
            id=uuid4(),
            user=uuid4(),
            pin_code="12345",  # Too short
            update_data='{"key": "value"}',
            attempts=3,
            created_at=datetime.now(),
        )
    with pytest.raises(ValidationError):
        UpdateActionModel(
            id=uuid4(),
            user=uuid4(),
            pin_code="1234567",  # Too long
            update_data='{"key": "value"}',
            attempts=3,
            created_at=datetime.now(),
        )
    with pytest.raises(ValidationError, match="PIN code must contain only digits"):
        UpdateActionModel(
            id=uuid4(),
            user=uuid4(),
            pin_code="abcdef",  # Invalid: not digits
            update_data='{"key": "value"}',
            attempts=3,
            created_at=datetime.now(),
        )


def test_update_action_model_invalid_json():
    with pytest.raises(ValidationError):
        UpdateActionModel(
            id=uuid4(),
            user=uuid4(),
            pin_code="123456",
            update_data="{invalid: json}",  # Invalid JSON
            attempts=3,
            created_at=datetime.now(),
        )
