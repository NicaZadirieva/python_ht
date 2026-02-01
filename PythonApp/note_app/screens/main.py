"""
Главный экран
"""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal
from note_app.config.config import AppSettings
from note_app.repositories.folder_repository import FolderRepository
from note_app.widgets import FileTreeWidget, NoteViewWidget


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

    def __init__(self, settings: AppSettings, *args, **kwargs) -> None:
        self.settings = settings
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        folder_repo = FolderRepository(self.settings.data_directory)
        yield Header()
        with Horizontal():
            yield FileTreeWidget(id="tree", folder_repo=folder_repo)
            yield NoteViewWidget()
        yield Footer()

    def on_mount(self):
        """
        Монтирование
        """
        self.title = "Менеджер заметок"
        self.query_one(NoteViewWidget).text = "## Привет!"

    def action_quit(self):
        """
        Выход из приложения
        """
        self.app.exit()
