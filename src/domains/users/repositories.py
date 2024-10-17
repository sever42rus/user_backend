from abc import ABC

from common_lib.models.users import UserModel

from core.repositories import AbstractBaseRepository
from core.repositories import PiccoloBaseRepository
from domains.users.tables import User


class AbstractUserRepository(AbstractBaseRepository[UserModel], ABC):
    """
    Абстрактный репозиторий для работы с объектами пользователя.
    Наследуется от AbstractBaseRepository, где тип T задан как UserModel.
    """


class PiccoloUserRepository(PiccoloBaseRepository[UserModel], AbstractUserRepository):
    """
    Репозиторий для работы с объектами пользователя на основе Piccolo ORM.
    Определяет таблицу User и модель UserModel для использования в CRUD операциях.
    """

    table: User = User
    model: UserModel = UserModel
