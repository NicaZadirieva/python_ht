from pathlib import Path
import sys

from note_app.app import NoteManagerApp
from note_app.config.config import AppSettings

def create_app(data_path: Path | None = None):
    settings: AppSettings
    if data_path:
        settings = AppSettings.from_custom_path(data_path=data_path)
    else:
        settings = AppSettings.from_defaults()
    return NoteManagerApp(settings)

def run():
    data_path = None
    if len(sys.argv) > 1:
        data_path = Path(sys.argv[1])
    app = create_app(data_path=data_path)
    app.run()
    