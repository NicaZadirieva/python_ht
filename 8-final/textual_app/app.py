"""
UI приложения
"""

import asyncio
from textual.app import App

from textual_app.repositories import (
    BaseMonitorDataRepository,
    FileMonitorDataRepository,
)
from textual_app.screens import MainScreen
from textual_app.services.monitor_service import MonitorService


class TextualManagerApp(App):
    """
    Класс для установки UI-приложения
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        """
        Монтирование главного экрана
        """
        monitor_data_repo: BaseMonitorDataRepository = FileMonitorDataRepository(
            "./temp.csv"
        )

        monitor_service: MonitorService = MonitorService()

        main_screen = MainScreen(
            monitor_data_repo=monitor_data_repo, monitor_service=monitor_service
        )
        self.push_screen(main_screen)
        asyncio.create_task(monitor_service.run())
