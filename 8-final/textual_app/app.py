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

    CSS = """
    Screen {
        background: $surface;
    }
    """

    async def on_mount(self) -> None:
        """
        Асинхронное монтирование главного экрана
        """
        monitor_data_repo: BaseMonitorDataRepository = FileMonitorDataRepository(
            "./temp.csv"
        )

        self.monitor_service = MonitorService(monitor_data_repo)

        main_screen = MainScreen(
            monitor_data_repo=monitor_data_repo, monitor_service=self.monitor_service
        )

        # Сначала показываем экран
        await self.push_screen(main_screen)

        # Затем запускаем мониторинг (после отрисовки UI)
        await self._start_monitoring_safely()

    async def _start_monitoring_safely(self):
        """
        Безопасный запуск мониторинга после инициализации UI
        """
        try:
            if self.monitor_service:
                # Создаем задачу, но не ждем ее завершения
                task = self.monitor_service.run()
                # Сохраняем задачу для управления
                self.monitor_task = task
                # Запускаем в фоне
                asyncio.create_task(self._wrap_monitoring_task(task))
        except Exception as e:
            self.log(f"Не удалось запустить мониторинг: {e}")

    async def _wrap_monitoring_task(self, task):
        """
        Обертка для задачи мониторинга с обработкой ошибок
        """
        try:
            await task
        except asyncio.CancelledError:
            pass  # Нормальная отмена
        except Exception as e:
            self.log(f"Фоновая задача мониторинга завершилась: {e}")

    def on_shutdown(self):
        """
        Корректная остановка
        """
        if hasattr(self, "monitor_task"):
            self.monitor_task.cancel()
        if hasattr(self, "monitor_service") and self.monitor_service:
            self.monitor_service.stop()
