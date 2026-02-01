"""
Таблица для просмотра результатов мониторинга
"""

from textual.events import Mount
from textual.widgets import DataTable, Static
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive


class MonitoringTable(Vertical):
    """
    Виджет для таблицы просмотра мониторинга
    """

    current_url: reactive[str] = reactive(default="")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Static("")
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

    def watch_current_url(self, _: str, new_text: str) -> None:
        """
        Обновление текста
        """
        self.query_one(Static).update(f"Added monitor for {new_text}")
