from polyfactory.factories.pydantic_factory import ModelFactory

from domains.users.models import UserLoginCredentialsModel


class UserLoginCredentialsModelFactory(ModelFactory[UserLoginCredentialsModel]):
    pass
