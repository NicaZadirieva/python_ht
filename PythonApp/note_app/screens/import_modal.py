"""
Модальное окно для импорта данных
"""

from textual.screen import ModalScreen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Input, Button


class ImportModal(ModalScreen):
    """
    Класс модального окна для импорта
    """

    CSS = """
      ImportModal {
        align: center middle;
      }
      #dialog {
		width: 60;
        height: 15;
        border: solid blue;
      }
      #title {
		dock: top;
        content-align: center middle;
        padding: 0 1;
        height: 2;
      }
      #buttons {
        align: center middle;
      }
  	"""

    def compose(self):
        with Container(id="dialog"):
            yield Static("Импорт данных", id="title")
            yield Input(placeholder="Введите url для импорта")
            with Horizontal(id="buttons"):
                yield Button("Импортировать", variant="primary")
                yield Button("Отмена")

    def key_escape(self) -> None:
        """
        Закрытие по нажатию на кнопку "Esc"
        """
        self.dismiss()
