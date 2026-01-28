from textual.app import App

from .config import AppSettings
from .screens import MainScreen

class NoteManagerApp(App):
	def __init__(self, settings: AppSettings, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.settings = settings

	def on_mount(self) -> None:
		main_screen = MainScreen()
		self.push_screen(main_screen)