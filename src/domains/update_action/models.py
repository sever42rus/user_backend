import json
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class EmailConfirmModel(BaseModel):
    email_confirmed: bool = Field(default=True)


class UpdateActionRequestModel(BaseModel):
    id: UUID


class UpdateActionCompleteModel(BaseModel):
    id: UUID
    pin_code: str = Field(..., min_length=6, max_length=6)

    @field_validator("pin_code")
    def validate_pin_code(cls, value: str):
        if not value.isdigit():
            raise ValueError("PIN code must contain only digits")
        return value


class UpdateActionModel(BaseModel):
    id: UUID
    user: UUID
    pin_code: str = Field(..., min_length=6, max_length=6)
    update_data: dict | Annotated[str, AfterValidator(json.loads)]
    attempts: int
    created_at: datetime

    @field_validator("pin_code")
    def validate_pin_code(cls, value: str):
        if not value.isdigit():
            raise ValueError("PIN code must contain only digits")
        return value
