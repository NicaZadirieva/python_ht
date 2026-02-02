"""
Виджет таблицы мониторинга
"""

from typing import Optional, Callable
from textual.widgets import DataTable
from textual.reactive import reactive

from textual_app.repositories import BaseMonitorDataRepository


class MonitoringTable(DataTable):
    """
    Виджет таблицы для отображения данных мониторинга
    """

    current_url = reactive("")
    last_item_count = 0

    def __init__(
        self,
        monitor_data_repo: BaseMonitorDataRepository,
        on_data_change: Optional[Callable] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._monitor_data_repo = monitor_data_repo
        self._on_data_change = on_data_change
        self._setup_table()

    def _setup_table(self):
        """Настройка таблицы"""
        self.add_columns("ID", "URL", "Interval", "Status", "HTTP Code", "Last Checked")
        self.update_table()

    def update_table(self):
        """Обновление данных таблицы"""
        # Очищаем таблицу
        self.clear()

        # Получаем все элементы из репозитория
        items = self._monitor_data_repo.load()
        self.last_item_count = len(items)

        # Добавляем строки
        for item in items:
            # Форматируем данные для отображения
            status = item.status.value if item.status else "PENDING"
            http_code = str(item.http_code) if item.http_code else ""
            last_checked = (
                item.latest_checked_time.strftime("%H:%M:%S")
                if item.latest_checked_time
                else "Never"
            )

            # Добавляем строку
            self.add_row(
                item.id, item.url, f"{item.interval}s", status, http_code, last_checked
            )

        # Уведомляем об изменении данных
        if self._on_data_change:
            self._on_data_change()
