from textual.containers import VerticalScroll
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Tree

from note_app.repositories import BaseFolderRepository


class FileTreeWidget(VerticalScroll):
    """
    Дерево просмотра заметок
    """

    _tree: Tree
    _folder_repo: BaseFolderRepository

    def __init__(self, folder_repo: BaseFolderRepository, *args, **kwargs) -> None:
        self._folder_repo = folder_repo
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        self._tree = Tree(label="Заметки")
        yield self._tree
