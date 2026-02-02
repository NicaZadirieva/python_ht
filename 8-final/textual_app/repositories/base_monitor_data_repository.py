"""
Хранение данных
"""

from abc import ABC, abstractmethod

from textual_app.domain import MonitorData


class BaseMonitorDataRepository(ABC):
    """
    Базовый класс для работы с данными мониторинга
    """

    @abstractmethod
    def load(self) -> list[MonitorData]:
        """
        Загрузка данных
        """

    @abstractmethod
    def delete(self, monitor_id: int | str) -> None:
        """
        Удаление данных по monitor_id
        """

    @abstractmethod
    def add_item(self, item: MonitorData) -> MonitorData:
        """
        Добавление данных
        """

    @abstractmethod
    def update_by_id(self, monitor_id: int | str, item: MonitorData) -> MonitorData:
        """
        Обновление данных по id
        """
