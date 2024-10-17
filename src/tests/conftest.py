from uuid import uuid4

import pytest
from common_lib.factories import UserModelFactory
from common_lib.models.users import UserModel
from httpx import AsyncClient
from piccolo.conf.apps import Finder
from piccolo.table import create_db_tables_sync
from piccolo.table import drop_db_tables_sync

from app import app
from domains.update_action.factories import UpdateActionModelFactory
from domains.update_action.models import UpdateActionModel
from domains.update_action.tables import UpdateAction
from domains.users.tables import User

# Получаем все классы таблиц из настроек приложения Piccolo
TABLES = Finder().get_table_classes()


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Создаем все таблицы, если они еще не существуют
    create_db_tables_sync(*TABLES, if_not_exists=True)
    # Переходим к выполнению модуля тестов
    yield
    # После выполнения тестов удаляем все таблицы
    drop_db_tables_sync(*TABLES)


@pytest.fixture()
def async_client() -> AsyncClient:
    # Возвращаем асинхронный клиент, который будет использоваться в тестах
    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture()
async def user_model_mock() -> UserModel:
    return UserModelFactory().build()


@pytest.fixture
async def user_fixture(user_model_mock: UserModel) -> User:
    """
    Фикстура для создания тестового пользователя.
    """
    user = User(
        id=uuid4(),
        email=user_model_mock.email,
        password=user_model_mock.password,
    )
    await user.save()
    yield user
    await User.delete().where(User.email == user.email).run()


@pytest.fixture()
async def update_action_mock() -> UpdateActionModel:
    return UpdateActionModelFactory().build()


@pytest.fixture
async def update_action_fixture(user_fixture: User) -> UpdateAction:
    update_action = UpdateAction(
        user=user_fixture.id,
        pin_code="123456",
        update_data={},
    )
    await update_action.save()
    yield update_action
    await UpdateAction.delete().where(UpdateAction.id == update_action.id).run()
