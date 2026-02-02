"""
Модальное окно для импорта данных
"""

from textual.screen import ModalScreen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Input, Button


class ImportModal(ModalScreen[str]):
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
            yield Input(placeholder="Введите url для импорта", id="input_url")
            with Horizontal(id="buttons"):
                yield Button("Импортировать", variant="primary", id="import_btn")
                yield Button("Отмена", id="cancel_btn")

    def key_escape(self) -> None:
        """
        Закрытие по нажатию на кнопку "Esc"
        """
        self.dismiss()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "import_btn":
            url_input = self.query_one("#input_url", Input)
            url = url_input.value.strip()
            if url:
                pass
            else:
                url_input.styles.border = ("solid", "red")
        else:
            self.dismiss(None)

    async def import_data(self, url: str) -> None:
        pass
