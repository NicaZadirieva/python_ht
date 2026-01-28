"""
Обработка markdown-файлов
"""

from textual.containers import VerticalScroll
from textual.app import ComposeResult
from textual.widgets import Markdown
from textual.reactive import reactive


class MarkdownWidget(VerticalScroll):
    """
    Виджет для просмотра markdown-файлов
    """

    text: reactive[str] = reactive(default="")

    def compose(self) -> ComposeResult:
        yield Markdown("sdsdsd")
