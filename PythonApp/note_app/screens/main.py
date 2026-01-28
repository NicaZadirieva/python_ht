"""
Главный экран
"""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header


class MainScreen(Screen):
    """
    Класс для главного экрана
    """

    def compose(self) -> ComposeResult:
        yield Header()

    def on_mount(self):
        """
        Монтирование
        """
        self.title = "Менеджер заметок"
