"""
Основной экран
"""

from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label, DataTable, Static
from textual.containers import Horizontal, Vertical

from textual_app.widgets.TextInput import TextInput


class MainScreen(Screen):
    """
    Класс для основного экрана
    """

    CSS = """
    .label {
        padding: 1;
    }
    .button-add {
        margin-left: 1
    }
    """
    BINDINGS = [("q", "quit", "Выход")]

    def compose(self) -> ComposeResult:
        yield Header()

        yield Horizontal(
            TextInput(label_text="URL", placeholder_text="URL..."),
            TextInput(label_text="Interval", placeholder_text="interval..."),
            Button(label="ADD", classes="button-add"),
        )
        yield Vertical(
            Static("Added monitor for https://app.purpleschool.ru"), DataTable()
        )

        yield Footer()

    def _on_mount(self, event: Mount) -> None:
        """
        Монтирование
        """
        self.title = "Менеджер проверки доступа URL"
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

    def action_quit(self):
        """
        Выход из приложения
        """
        self.app.exit()
