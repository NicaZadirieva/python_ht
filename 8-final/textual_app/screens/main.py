"""
Основной экран
"""

from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Horizontal

from textual_app.widgets import MonitoringTable, TextInput


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
        yield MonitoringTable()

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
