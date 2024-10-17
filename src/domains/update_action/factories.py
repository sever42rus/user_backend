from polyfactory.factories.pydantic_factory import ModelFactory

from domains.update_action.models import UpdateActionModel
from domains.update_action.models import UpdateActionRequestModel


class UpdateActionModelFactory(ModelFactory[UpdateActionModel]):
    pin_code = "123456"
    update_data = {}


class UpdateActionRequestModelFactory(ModelFactory[UpdateActionRequestModel]):
    pass
