from datetime import datetime

from piccolo.columns import UUID
from piccolo.columns import Boolean
from piccolo.columns import Timestamptz
from piccolo.columns import Varchar
from piccolo.table import Table


class User(Table, tablename="users"):
    """
    Модель таблицы 'User', которая хранит информацию о пользователях в системе.
    Каждый пользователь имеет уникальный идентификатор, email, пароль, уровень доступа,
    статус подтверждения email и дату создания.
    """

    id = UUID(primary_key=True, default=None, unique=True, index=True, help_text="UUID PK")
    email = Varchar(length=255, default=None, unique=True, index=True, help_text="Email")
    email_confirmed = Boolean(default=False, help_text="Email подтвержден")
    password = Varchar(length=255, default=None, help_text="Пароль пользователя")
    access_level = Varchar(length=100, default=None, null=True, help_text="Уровень доступа")
    created_at = Timestamptz(default=datetime.now, help_text="Дата и время создания")
