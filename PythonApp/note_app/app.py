"""
Модуль для работы с основным классом для приложения
"""

from textual.app import App

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
        main_screen = MainScreen(self.settings)
        self.push_screen(main_screen)
