"""
Главный экран
"""

from typing import Optional
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal
from note_app.config.config import AppSettings
from note_app.repositories import BaseFolderRepository, BaseNoteRepository
from note_app.screens.import_modal import ImportModal
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
    BINDINGS = [("q", "quit", "Выход"), ("i", "import", "Импортировать")]

    def __init__(
        self,
        settings: AppSettings,
        folder_repo: BaseFolderRepository,
        note_repo: BaseNoteRepository,
        *args,
        **kwargs,
    ) -> None:
        self._folder_repo = folder_repo
        self._note_repo = note_repo
        self.settings = settings
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield FileTreeWidget(
                id="tree", folder_repo=self._folder_repo, note_repo=self._note_repo
            )
            yield NoteViewWidget()
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

    def action_import(self):
        """
        Импорт
        """
        self.app.push_screen(ImportModal())

    def handle_import(self, data: Optional[str]):
        if data:
            self.app.notify(data)

    def on_file_tree_widget_note_selected(
        self, message: FileTreeWidget.NoteSelected
    ) -> None:
        note = self._note_repo.load_note(message.note_path)
        if note.content:
            self.query_one(NoteViewWidget).text = note.content
        else:
            self.query_one(NoteViewWidget).text = ""
