from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header

class MainScreen(Screen):
	def compose(self) -> ComposeResult:
		yield Header()