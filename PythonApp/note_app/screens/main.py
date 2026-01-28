"""
Главный экран
"""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Tree
from textual.containers import Horizontal

from note_app.widgets import MarkdownWidget


class MainScreen(Screen):
    """
    Класс для главного экрана
    """

    CSS = """
    #tree {
        width: 25%
    }
    """
    BINDINGS = [("q", "quit", "Выход")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Tree(label="Моя база знаний", id="tree")
            yield MarkdownWidget()
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
