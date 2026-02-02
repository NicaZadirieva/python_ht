from pathlib import Path
from textual.containers import VerticalScroll
from textual.app import ComposeResult
from textual.events import Mount
from textual.widgets import Tree
from textual.widgets._tree import TreeNode
from textual.message import Message
from note_app.repositories import BaseFolderRepository, BaseNoteRepository


class FileTreeWidget(VerticalScroll):
    """
    Дерево просмотра заметок и папок
    """

    _tree: Tree
    _folder_repo: BaseFolderRepository
    _note_repo: BaseNoteRepository

    class NoteSelected(Message):
        """Событие выбора заметок"""

        def __init__(self, note_path: Path):
            self.note_path = note_path
            super().__init__()

    class FolderSelected(Message):
        """Событие выбора папки"""

        def __init__(self, folder_path: Path):
            self.folder_path = folder_path
            super().__init__()

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

    def collapse(self):
        root = self.query_one(Tree).root
        root.collapse()

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node: TreeNode[Path] = event.node
        node.remove_children()
        path = node.data if node.data else ""
        folders = self._folder_repo.get_folders_by_path(Path(path))

        for folder in folders:
            node.add(folder.name, folder.path)
        notes = self._note_repo.get_notes_by_path(Path(path))

        for note in notes:
            node.add_leaf(note.name, note.path)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node: TreeNode[Path] = event.node
        if node.data and node.data.suffix == ".md":
            self.post_message(self.NoteSelected(node.data))

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        node: TreeNode[Path] = event.node
        if node.data and not node.data.suffix == ".md":
            self.post_message(self.FolderSelected(node.data))
