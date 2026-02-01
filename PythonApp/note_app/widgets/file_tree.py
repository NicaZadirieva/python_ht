from pathlib import Path
from textual.containers import VerticalScroll
from textual.app import ComposeResult
from textual.events import Mount
from textual.widgets import Tree
from textual.widgets._tree import TreeNode

from note_app.domain.folder import Folder
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

    def _on_mount(self, event: Mount) -> None:
        root = self._tree.root
        root.data = Folder("data", Path("data"))
        root.expand()

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node: TreeNode[Folder] = event.node
        node.remove_children()
        path = node.data.path if node.data else ""
        folders = self._folder_repo.get_folders_by_path(Path(path))

        for folder in folders:
            node.add(folder.name, folder)
