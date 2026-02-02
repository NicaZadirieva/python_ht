"""
Основной экран
"""

import logging
from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static
from textual.containers import Horizontal
from textual import work

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
        self._monitoring_started = False

        # Инициализация логгера
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            self.logger.setLevel(logging.INFO)

        self.logger.info("MainScreen initialized")

        # Подписываемся на обновления сервиса мониторинга
        self._setup_monitoring_updates()

    def compose(self) -> ComposeResult:
        self.logger.debug("Starting compose")
        yield Header()
        # Статус бар
        yield Static("Мониторинг: остановлен", id="monitor_status")
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
        # Создаем таблицу с колбэком для обновления
        yield MonitoringTable(
            self._monitor_data_repo, on_data_change=self._on_table_data_change
        )

        yield Footer()
        self.logger.debug("Compose completed")

    def _on_mount(self, event: Mount) -> None:
        """
        Монтирование
        """
        self.title = "Менеджер проверки доступа URL"
        self.logger.info(f"MainScreen mounted with title: {self.title}")

        # Запускаем периодическое обновление таблицы
        self.set_interval(1, self._refresh_table)
        self.logger.debug("Set table refresh interval to 1 second")

    def _setup_monitoring_updates(self):
        """Настройка получения обновлений от сервиса мониторинга"""
        self.logger.debug("Setting up monitoring updates")
        # Здесь можно добавить механизм подписки на обновления
        # Например, через асинхронную очередь или события
        pass

    def _refresh_table(self):
        """Периодическое обновление таблицы"""
        try:
            monitor_table = self.query_one(MonitoringTable)
            if monitor_table:
                # Проверяем, нужно ли обновлять таблицу
                current_count = len(self._monitor_data_repo.load())
                if current_count != monitor_table.last_item_count:
                    self.logger.debug(
                        f"Table refresh needed: current_count={current_count}, last_item_count={monitor_table.last_item_count}"
                    )
                    monitor_table.update_table()
        except Exception as e:
            # Игнорируем ошибки при обновлении, чтобы не падало приложение
            self.logger.error(f"Error refreshing table: {e}")

    def _on_table_data_change(self):
        """Колбэк при изменении данных в таблице"""
        self.logger.debug("Table data change callback triggered")
        self._refresh_table()

    def action_quit(self):
        """
        Выход из приложения
        """
        self.logger.info("Quit action triggered")
        self.app.exit()

    def add_new_monitor_data(self, url: str, interval: int):
        """Добавление новых данных для мониторинга"""
        try:
            self.logger.info(f"Adding new monitor data: url={url}, interval={interval}")
            # Определяем следующий ID
            existing_items = self._monitor_data_repo.load()
            next_id = max([item.id for item in existing_items], default=0) + 1
            self.logger.debug(f"Next ID: {next_id}")

            item = MonitorData(
                id=next_id, url=url, interval=interval, status=HttpStatus.PENDING
            )

            # Добавляем в репозиторий
            added_item = self._monitor_data_repo.add_item(item)
            self.logger.info(f"Item added to repository: id={added_item.id}")

            # Добавляем в сервис мониторинга
            self._monitor_service.add(added_item)
            self.logger.info(f"Item added to monitor service: id={added_item.id}")

            # Обновляем таблицу
            monitor_table = self.query_one(MonitoringTable)
            monitor_table.update_table()
            self.logger.debug("Table updated")

            # Если мониторинг еще не запущен, запускаем его
            if not self._monitoring_started:
                self.logger.info("Monitoring not started yet, starting now")
                self._start_monitoring()
                self._monitoring_started = True
                self.logger.info("Monitoring started")

            self.update_monitor_status(self._monitoring_started)

        except Exception as e:
            # Обработка ошибок при добавлении
            self.logger.error(f"Error adding monitor data: {e}")

    @work
    async def _start_monitoring(self):
        """Запуск мониторинга в фоновом режиме"""
        try:
            self.logger.info("Starting monitoring in background")
            # Запускаем мониторинг в фоновом режиме
            await self._monitor_service.run()
            self.logger.info("Monitoring completed")
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_btn":
            self.logger.debug("Add button pressed")
            url_input = self.query_one("#input_url", Input)
            url = url_input.value.strip()
            interval_input = self.query_one("#input_interval", Input)

            try:
                interval = int(interval_input.value.strip())
                self.logger.debug(f"Parsed interval: {interval}")
            except ValueError:
                # Невалидный интервал
                self.logger.warning(f"Invalid interval value: {interval_input.value}")
                interval_input.styles.border = ("solid", "red")
                return

            if url and interval > 0:
                self.logger.debug(f"Valid input: url={url}, interval={interval}")
                self.add_new_monitor_data(url, interval)

                # Сбрасываем поля ввода
                url_input.value = ""
                interval_input.value = ""
                url_input.styles.border = ("none", "white")
                interval_input.styles.border = ("none", "white")
                self.logger.debug("Input fields reset")
            else:
                # Подсвечиваем невалидные поля
                self.logger.warning(
                    f"Invalid input: url empty={not url}, interval valid={interval > 0}"
                )
                if not url:
                    url_input.styles.border = ("solid", "red")
                if interval <= 0:
                    interval_input.styles.border = ("solid", "red")

    def update_monitor_status(self, is_running: bool):
        self.logger.debug(f"Updating monitor status: is_running={is_running}")
        status_widget = self.query_one("#monitor_status", Static)
        if is_running:
            status_widget.update("Мониторинг: запущен ✓")
            status_widget.styles.color = "green"
        else:
            status_widget.update("Мониторинг: остановлен ✗")
            status_widget.styles.color = "red"
        self.logger.debug("Monitor status updated")
