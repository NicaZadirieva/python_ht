"""
Основной экран
"""

from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input
from textual.containers import Horizontal

from textual_app.domain import MonitorData, HttpStatus
from textual_app.repositories import BaseMonitorDataRepository
from textual_app.services.monitor_service import MonitorService
from textual_app.widgets import MonitoringTable, TextInput


class MainScreen(Screen):
    """
    Класс для основного экрана
    """

    CSS = """
    .label {
        padding: 1;
    }
    .button-add {
        margin-left: 1
    }
    """
    BINDINGS = [("q", "quit", "Выход")]

    def __init__(
        self,
        monitor_data_repo: BaseMonitorDataRepository,
        monitor_service: MonitorService,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._monitor_data_repo = monitor_data_repo
        self._monitor_service = monitor_service

    def compose(self) -> ComposeResult:
        yield Header()

        yield Horizontal(
            TextInput(
                label_text="URL", placeholder_text="URL...", input_id="input_url"
            ),
            TextInput(
                label_text="Interval",
                placeholder_text="interval...",
                input_id="input_interval",
            ),
            Button(label="ADD", classes="button-add", id="add_btn"),
        )
        yield MonitoringTable(self._monitor_data_repo)

        yield Footer()

    def _on_mount(self, event: Mount) -> None:
        """
        Монтирование
        """
        self.title = "Менеджер проверки доступа URL"

    def action_quit(self):
        """
        Выход из приложения
        """
        self.app.exit()

    def add_new_monitor_data(self, url: str, interval: int):
        item = MonitorData(0, url, interval, status=HttpStatus.PENDING)
        item = self._monitor_data_repo.add_item(item)
        monitor_table = self.query_one(MonitoringTable)
        monitor_table.current_url = url
        monitor_table.update_table()
        self._monitor_service.add(item)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_btn":
            url_input = self.query_one("#input_url", Input)
            # TODO: сделать валидацию URL
            url = url_input.value.strip()
            interval_input = self.query_one("#input_interval", Input)
            # TODO: сделать валидацию интервала
            interval = int(interval_input.value.strip())
            if url and interval:
                self.app.call_later(self.add_new_monitor_data, url, interval)
            else:
                url_input.styles.border = ("solid", "red")
