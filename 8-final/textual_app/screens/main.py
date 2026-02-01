"""
Основной экран
"""

from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer


class MainScreen(Screen):
    """
    Класс для основного экрана
    """

    BINDINGS = [("q", "quit", "Выход")]

    def compose(self) -> ComposeResult:
        yield Header()
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
