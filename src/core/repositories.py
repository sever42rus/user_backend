from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict

from piccolo.table import Table
from pydantic import BaseModel

from core.exceptions import MultipleObjectsException


class AbstractBaseRepository[T](ABC):
    """
    Абстрактный репозиторий, определяющий интерфейс для работы с данными.
    Обеспечивает базовые методы для CRUD операций.
    """

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> T:
        """
        Создает новый объект на основе переданных данных.
        Возвращает объект типа T.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_fields(self, filter_params: Dict[str, Any]) -> T | None:
        """
        Получает объект по указанным фильтрам.
        Возвращает объект типа T или None, если объект не найден.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(self, filter_params: Dict[str, Any]) -> bool:
        """
        Проверяет наличие объекта, удовлетворяющего фильтрам.
        Возвращает True, если объект существует, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, filter_params: Dict[str, Any], update_data=Dict[str, Any]) -> bool:
        """
        Обновляет объект, удовлетворяющий фильтрам, новыми данными.
        Возвращает True в случае успешного обновления.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, filter_params: Dict[str, Any]) -> bool:
        """
        Удаляет объект на основе переданных фильтров.
        Возвращает True после успешного удаления.
        """
        raise NotImplementedError


class PiccoloBaseRepository[T](AbstractBaseRepository):
    """
    Реализация абстрактного репозитория с использованием Piccolo ORM.
    Определяет методы для создания, получения, проверки и обновления объектов в базе данных.
    """

    table: Table = Table
    model: BaseModel = BaseModel

    async def create(self, data: Dict[str, Any]) -> T:
        """
        Создает запись в таблице на основе данных.
        Возвращает объект модели с заполненными данными.
        """
        insert_obj = self.table(**data)
        object_list = await self.table.insert(insert_obj).returning(*self.table.all_columns()).run()
        return self.model(**object_list[0])

    async def get_by_fields(self, filter_params: Dict[str, Any]) -> T | None:
        """
        Получает объект по переданным полям фильтрации.
        Возвращает объект модели или None, если объект не найден.
        """
        filters = [getattr(self.table, key) == value for key, value in filter_params.items()]
        results = await self.table.select().where(*filters).run()
        if len(results) > 1:
            raise MultipleObjectsException(f"multiple objects {self.table.__name__} returned")
        return self.model(**results[0]) if results else None

    async def exists(self, filter_params: Dict[str, Any]) -> bool:
        """
        Проверяет наличие объекта в таблице по указанным фильтрам.
        Возвращает True, если объект существует, иначе False.
        """
        filters = [getattr(self.table, key) == value for key, value in filter_params.items()]
        return await self.table.exists().where(*filters).run()

    async def update(self, filter_params: Dict[str, Any], update_data=Dict[str, Any]) -> bool:
        """
        Обновляет объект в таблице на основе переданных фильтров и новых данных.
        Возвращает True после успешного обновления.
        """
        filters = [getattr(self.table, key) == value for key, value in filter_params.items()]
        updates = {getattr(self.table, key): value for key, value in update_data.items()}
        await self.table.update(updates).where(*filters)
        return True

    async def delete(self, filter_params: Dict[str, Any]) -> bool:
        """
        Удаляет объект на основе переданных фильтров.
        Возвращает True после успешного удаления.
        """
        filters = [getattr(self.table, key) == value for key, value in filter_params.items()]
        await self.table.delete().where(*filters)
        return True
