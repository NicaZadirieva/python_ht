"""
Основной экран
"""

from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label, DataTable, Static
from textual.containers import Horizontal, Vertical


class MainScreen(Screen):
    """
    Класс для основного экрана
    """

    CSS = """
    .form-input {
        width: 100;
    }
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
            Horizontal(
                Label("URL", classes="label"),
                Input(placeholder="URL..."),
                classes="form-input",
            ),
            Horizontal(
                Label("Interval", classes="label"),
                Input(placeholder="interval..."),
                classes="form-input",
            ),
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
