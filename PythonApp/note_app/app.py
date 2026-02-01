"""
Модуль для работы с основным классом для приложения
"""

from textual.app import App

from note_app.repositories import FolderRepository, NoteRepository

from .config import AppSettings
from .screens import MainScreen


class NoteManagerApp(App):
    """
    Класс для вывода приложения
    """

    def __init__(self, settings: AppSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings

    def on_mount(self) -> None:
        """
        Коллбек после монтирования приложения
        """
        folder_repo = FolderRepository(self.settings.data_directory)
        note_repo = NoteRepository(self.settings.data_directory)
        main_screen = MainScreen(
            self.settings, folder_repo=folder_repo, note_repo=note_repo
        )
        self.push_screen(main_screen)
