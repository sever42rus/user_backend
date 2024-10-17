from uuid import uuid4

import pytest
from asyncpg.exceptions import UniqueViolationError

from domains.users.tables import User


@pytest.mark.asyncio
async def test_user_creation(user_fixture):
    """
    Проверяет, что запись может быть успешно создана.
    """
    saved_user = await User.objects().where(User.email == user_fixture.email).first().run()

    assert saved_user.email == user_fixture.email, "Пользователь не был сохранен правильно."
    assert saved_user.id is not None, "Поле created_at не должно быть None."
    assert saved_user.created_at is not None, "Поле created_at не должно быть None."


@pytest.mark.asyncio
async def test_unique_constraints(user_fixture):
    """
    Проверяет, что ограничения уникальности соблюдаются.
    """
    with pytest.raises(UniqueViolationError):
        await User(
            id=uuid4(),
            email=user_fixture.email,  # Такой же email
            password=user_fixture.password,
        ).save()
