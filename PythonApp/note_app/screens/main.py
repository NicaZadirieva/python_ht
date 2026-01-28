"""
Главный экран
"""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer


class MainScreen(Screen):
    """
    Класс для главного экрана
    """

    BINDINGS = [("q", "quit", "Выход")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self):
        """
        Монтирование
        """
        self.title = "Менеджер заметок"

    def action_quit(self):
        """
        Выход из приложения
        """
        self.app.exit()
