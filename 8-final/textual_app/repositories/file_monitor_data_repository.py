"""
Хранение данных через файл
"""

from textual_app.repositories.base_monitor_data_repository import (
    BaseMonitorDataRepository,
)


class FileMonitorDataRepository(BaseMonitorDataRepository):
    """
    Реализация работы с данными мониторинга через сохранение в файл
    """
