"""
Текстовое поле
"""

from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.widgets import Label, Input


class TextInput(Horizontal):
    """
    Класс для текстового поля
    """

    CSS = """
    .form-input {
        width: 100;
    }
    """

    def __init__(
        self, label_text: str, placeholder_text: str, input_id: str, *args, **kwargs
    ) -> None:
        super().__init__(classes="form-input", *args, **kwargs)
        self.label_text = label_text
        self.placeholder_text = placeholder_text
        self.input_id = input_id

    def compose(self) -> ComposeResult:
        yield Label(self.label_text, classes="label")
        yield Input(placeholder=self.placeholder_text, id=self.input_id)
