from datetime import datetime

from piccolo.columns import JSON
from piccolo.columns import UUID
from piccolo.columns import ForeignKey
from piccolo.columns import OnDelete
from piccolo.columns import OnUpdate
from piccolo.columns import SmallInt
from piccolo.columns import Timestamptz
from piccolo.columns import Varchar
from piccolo.table import Table

from domains.users.tables import User


class UpdateAction(Table, tablename="update_action"):
    id = UUID(primary_key=True, unique=True, index=True, help_text="UUID PK")
    user = ForeignKey(
        references=User,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        index=True,
        null=False,
        help_text="Пользователь",
    )
    pin_code = Varchar(length=6, help_text="PIN код")
    update_data = JSON(default={}, help_text="Тип контакта")
    attempts = SmallInt(default=3, help_text="Количество попыток")
    created_at = Timestamptz(default=datetime.now, help_text="Дата и время создания")
