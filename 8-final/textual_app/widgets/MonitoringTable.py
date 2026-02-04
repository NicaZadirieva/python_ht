"""
Виджет таблицы мониторинга
"""

from typing import Optional, Callable
from textual.widgets import DataTable
from textual.reactive import reactive
from textual.message import Message
from textual_app.repositories import BaseMonitorDataRepository


class MonitoringTable(DataTable):
    """
    Виджет таблицы для отображения данных мониторинга
    """

    current_url = reactive("")
    last_item_count = 0

    class MonitorRowSelected(Message):
        """Событие выбора заметок"""

        def __init__(self, row_id: int):
            self.row_id = row_id
            super().__init__()

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
        # Включаем курсор для навигации
        self.cursor_type = "row"
        self.show_cursor = True

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

    def get_selected_row_id(self) -> Optional[int]:
        """
        Получение ID выделенной строки через cursor_row
        """
        if self.cursor_row is None:
            return None

        try:
            # Получаем данные из выделенной строки
            row_data = self.get_row_at(self.cursor_row)
            if row_data and len(row_data) > 0:
                # Первый элемент в строке - это ID
                row_id = row_data[0]
                # Преобразуем в int, если это строка
                if isinstance(row_id, str):
                    return int(row_id)
                return row_id
        except (ValueError, IndexError, TypeError) as e:
            self.log.error(f"Error getting selected row ID: {e}")

        return None

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.log.info(f"Row selected: {event.row_key}")
        if event.row_key.value:
            try:
                row_id = int(event.row_key.value)
                self.post_message(self.MonitorRowSelected(row_id))
            except ValueError:
                self.log.error(f"Row key is not an integer: {event.row_key.value}")
