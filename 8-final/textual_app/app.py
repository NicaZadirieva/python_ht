"""
UI приложения
"""

from textual.app import App

from textual_app.screens import MainScreen


class TextualManagerApp(App):
    """
    Класс для установки UI-приложения
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        """
        Монтирование главного экрана
        """
        main_screen = MainScreen()
        self.push_screen(main_screen)
