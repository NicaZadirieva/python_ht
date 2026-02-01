"""
Запуск приложения
"""

from textual_app.app import TextualManagerApp


def create_app():
    """
    Точка входа в приложение
    """
    return TextualManagerApp()


def run():
    """
    Функция запуска приложения
    """
    app = create_app()
    app.run()
