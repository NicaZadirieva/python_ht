"""
Таблица для просмотра результатов мониторинга
"""

from textual.events import Mount
from textual.widgets import DataTable, Static
from textual.app import ComposeResult
from textual.containers import Vertical


class MonitoringTable(Vertical):
    """
    Виджет для таблицы просмотра мониторинга
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Static("Added monitor for https://app.purpleschool.ru")
        yield DataTable()

    def _on_mount(self, event: Mount) -> None:
        table = self.query_one(DataTable)
        table.focus()
        table.add_columns(
            "url",
            "interval",
            "status",
            "http",
            "latest checked time",
        )
        table.add_row("https://app.purpleschool.ru", 10, "OK", "200", "10:43:09")
        table.fixed_columns = 5
        table.cursor_type = "row"
