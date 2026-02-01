from pathlib import Path
from textual.containers import VerticalScroll
from textual.app import ComposeResult
from textual.events import Mount
from textual.widgets import Tree
from textual.widgets._tree import TreeNode

from note_app.domain.folder import Folder
from note_app.repositories import BaseFolderRepository, BaseNoteRepository


class FileTreeWidget(VerticalScroll):
    """
    Дерево просмотра заметок
    """

    _tree: Tree
    _folder_repo: BaseFolderRepository
    _note_repo: BaseNoteRepository

    def __init__(
        self,
        folder_repo: BaseFolderRepository,
        note_repo: BaseNoteRepository,
        *args,
        **kwargs,
    ) -> None:
        self._folder_repo = folder_repo
        self._note_repo = note_repo
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        self._tree = Tree(label="Заметки")
        yield self._tree

    def _on_mount(self, event: Mount) -> None:
        root = self._tree.root
        root.data = Path("data")
        root.expand()

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node: TreeNode[Path] = event.node
        node.remove_children()
        path = node.data if node.data else ""
        folders = self._folder_repo.get_folders_by_path(Path(path))

        for folder in folders:
            node.add(folder.name, folder.path)
        notes = self._note_repo.get_notes_by_path(Path(path))

        for note in notes:
            node.add(note.name, note.path)
