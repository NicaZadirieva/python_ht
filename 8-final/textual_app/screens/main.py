"""
Основной экран
"""

from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label
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
            Button("ADD", classes="button-add"),
        )

        yield Footer()

    def _on_mount(self, event: Mount) -> None:
        """
        Монтирование
        """
        self.title = "Менеджер проверки доступа URL"

    def action_quit(self):
        """
        Выход из приложения
        """
        self.app.exit()
