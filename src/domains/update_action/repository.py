from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict

from core.repositories import AbstractBaseRepository
from core.repositories import PiccoloBaseRepository
from domains.update_action.models import UpdateActionModel
from domains.update_action.tables import UpdateAction


class AbstractUpdateActionRepository(AbstractBaseRepository[UpdateActionModel], ABC):
    @abstractmethod
    async def attempts_decrement(self, filter_params: Dict[str, Any]) -> UpdateActionModel:
        raise NotImplementedError


class PiccoloUpdateActionRepository(PiccoloBaseRepository[UpdateActionModel], AbstractUpdateActionRepository):
    table: UpdateAction = UpdateAction
    model: UpdateActionModel = UpdateActionModel

    async def attempts_decrement(self, filter_params: Dict[str, Any]) -> UpdateActionModel | None:
        filters = [getattr(self.table, key) == value for key, value in filter_params.items()]
        update_action = (
            await self.table.update({self.table.attempts: self.table.attempts - 1})
            .where(*filters)
            .returning(*self.table.all_columns())
        )
        return self.model(**update_action[0]) if update_action else None
