"""
Основной экран
"""

import logging
import asyncio
import os
import sys
import traceback
from logging.handlers import RotatingFileHandler
from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static
from textual.containers import Horizontal
from textual import work
from typing import Optional

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
    .status-running {
        color: green;
    }
    .status-stopped {
        color: red;
    }
    .error-message {
        color: $error;
        background: $surface;
        border: solid red;
        padding: 1;
        margin: 1;
    }
    """
    BINDINGS = [("q", "quit", "Выход"), ("d", "delete", "Удалить")]

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
        self._monitor_task: Optional[asyncio.Task] = None
        self._update_interval = 1  # Интервал обновления в секундах
        self._last_data_hash = ""  # Хэш для отслеживания изменений данных
        self._table_mounted = False  # Флаг, что таблица смонтирована
        self._row: Optional[int] = None
        # Инициализация логгера с записью в файл
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Настройка логгера"""
        logger = logging.getLogger(f"{self.__class__.__name__}")
        logger.setLevel(logging.DEBUG)

        # Удаляем существующие обработчики, чтобы избежать дублирования
        logger.handlers.clear()

        # Форматтер для логов
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Обработчик для вывода в консоль
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Обработчик для записи в файл с ротацией
        try:
            file_handler = RotatingFileHandler(
                "monitor_service.log",
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=3,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Не удалось создать файловый обработчик логов: {e}")

        return logger

    def compose(self) -> ComposeResult:
        self.logger.debug("Starting compose")
        yield Header()
        # Статус бар
        yield Static(
            "Мониторинг: остановлен", id="monitor_status", classes="status-stopped"
        )
        yield Horizontal(
            TextInput(
                label_text="URL",
                placeholder_text="https://example.com",
                input_id="input_url",
            ),
            TextInput(
                label_text="Interval (sec)",
                placeholder_text="60",
                input_id="input_interval",
            ),
            Button(label="ADD", variant="primary", classes="button-add", id="add_btn"),
        )
        # Создаем таблицу с колбэком для обновления
        yield MonitoringTable(
            self._monitor_data_repo,
            on_data_change=self._on_table_data_change,
            id="monitoring_table",
        )

        yield Footer()
        self.logger.debug("Compose completed")

    def _on_mount(self, event: Mount) -> None:
        """
        Монтирование
        """
        self.title = "Менеджер проверки доступа URL"
        self.logger.info(f"MainScreen mounted with title: {self.title}")

        # Устанавливаем флаг, что таблица смонтирована через небольшую задержку
        self.set_timer(0.5, self._set_table_mounted)

        # Запускаем периодическое обновление таблицы с задержкой
        self.set_timer(1.0, self._start_table_refresh)

        self.logger.debug("Table refresh scheduled")

        # Проверяем, есть ли уже элементы для мониторинга
        existing_items = self._monitor_data_repo.load()
        if existing_items:
            self.logger.info(f"Found {len(existing_items)} existing monitoring items")
            # Добавляем существующие элементы в сервис мониторинга
            for item in existing_items:
                self.logger.debug(
                    f"Adding existing item to monitor service: id={item.id}, url={item.url}"
                )
                self._monitor_service.add(item)
            # Запускаем мониторинг для существующих элементов
            if not self._monitoring_started:
                self._start_monitoring()
                self._monitoring_started = True
                self.update_monitor_status(self._monitoring_started)
                self.logger.info("Started monitoring for existing items")

    def _set_table_mounted(self):
        """Устанавливаем флаг, что таблица смонтирована"""
        self._table_mounted = True
        self.logger.debug("Table mounted flag set to True")
        # Принудительно обновляем таблицу после монтирования
        self._refresh_table()

    def _start_table_refresh(self):
        """Запуск периодического обновления таблицы"""
        self.set_interval(self._update_interval, self._refresh_table)
        self.logger.debug(
            f"Table refresh interval started: {self._update_interval} seconds"
        )

    def _get_data_hash(self) -> str:
        """Создание хэша данных для отслеживания изменений"""
        try:
            items = self._monitor_data_repo.load()
            # Создаем строку с данными, которые могут меняться
            data_string = ""
            for item in items:
                status_val = item.status.value if item.status else "None"
                http_code_val = str(item.http_code) if item.http_code else "None"
                checked_time = (
                    str(item.latest_checked_time)
                    if item.latest_checked_time
                    else "None"
                )

                data_string += f"{item.id}:{status_val}:{http_code_val}:{checked_time}"
            return str(hash(data_string))
        except Exception as e:
            self.logger.error(f"Error calculating data hash: {e}")
            return ""

    def _refresh_table(self):
        """Периодическое обновление таблицы"""
        if not self._table_mounted:
            self.logger.debug("Table not mounted yet, skipping refresh")
            return

        try:
            monitor_table = self.query_one("#monitoring_table")
            if monitor_table is not None:
                # Проверяем, изменились ли данные
                current_hash = self._get_data_hash()
                current_count = len(self._monitor_data_repo.load())

                # Обновляем, если изменилось количество элементов или хэш данных
                needs_refresh = (
                    current_count != monitor_table.last_item_count
                    or current_hash != self._last_data_hash
                )

                if needs_refresh:
                    self.logger.debug(
                        f"Table refresh needed: "
                        f"items_count={current_count}/{monitor_table.last_item_count}, "
                        f"data_changed={current_hash != self._last_data_hash}"
                    )
                    monitor_table.update_table()
                    self._last_data_hash = current_hash
                    self.logger.debug("Table updated with latest data")
                else:
                    # Отладочное сообщение можно убрать или оставить на более высоком уровне
                    pass
            else:
                # Таблица существует, но не найдена - это может быть временной проблемой
                self.logger.debug("MonitoringTable not found in DOM")
        except Exception as e:
            # Логируем ошибку, но не падаем
            self.logger.debug(f"Error refreshing table: {e}")

    def _on_table_data_change(self):
        """Колбэк при изменении данных в таблице"""
        self.logger.debug("Table data change callback triggered")
        self._refresh_table()

    def action_quit(self):
        """
        Выход из приложения
        """
        self.logger.info("Quit action triggered")
        # Останавливаем мониторинг перед выходом
        self._stop_monitoring()
        self.app.exit()

    def action_delete(self):
        """
        Удалить строку из таблицы
        """
        self.logger.info("Delete action triggered")
        if self._row:
            self._monitor_data_repo.delete(self._row)
            self._monitor_service.delete_by_monitor_id(self._row)
            self._refresh_table()

    def add_new_monitor_data(self, url: str, interval: int):
        """Добавление новых данных для мониторинга"""
        try:
            self.logger.info(f"Adding new monitor data: url={url}, interval={interval}")

            # Валидация URL
            if not self._validate_url(url):
                self.logger.error(f"Invalid URL format: {url}")
                self._show_error_message(f"Неверный формат URL: {url}")
                return

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
            self._refresh_table()
            self.logger.debug("Table updated")

            # Если мониторинг еще не запущен, запускаем его
            if not self._monitoring_started:
                self.logger.info("Monitoring not started yet, starting now")
                self._start_monitoring()
                self._monitoring_started = True
                self.logger.info("Monitoring started")
            else:
                self.logger.debug("Monitoring already started, no need to start again")

            self.update_monitor_status(self._monitoring_started)

        except Exception as e:
            # Обработка ошибок при добавлении
            error_msg = f"Error adding monitor data: {str(e)}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            self._show_error_message(f"Ошибка при добавлении: {str(e)}")

    def _validate_url(self, url: str) -> bool:
        """Валидация URL"""
        import re

        # Простая валидация URL
        url_pattern = re.compile(
            r"^https?://"  # http:// или https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # домен
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # или IP
            r"(?::\d+)?"  # порт (опционально)
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return bool(url_pattern.match(url))

    def _show_error_message(self, message: str):
        """Показать сообщение об ошибке в UI"""
        try:
            # Удаляем предыдущие сообщения об ошибках
            error_widgets = self.query(".error-message")
            for widget in error_widgets:
                widget.remove()

            # Создаем новое сообщение
            error_widget = Static(message, classes="error-message")
            self.mount(error_widget, before="#monitoring_table")

            # Удаляем через 5 секунд
            self.set_timer(5, lambda: error_widget.remove())
        except Exception as e:
            self.logger.error(f"Error showing error message: {e}")

    def _start_monitoring(self):
        """Запуск мониторинга в фоновом режиме"""
        self.logger.info("_start_monitoring method called")

        # Проверяем состояние сервиса мониторинга
        if (
            hasattr(self._monitor_service, "_running")
            and self._monitor_service._running
        ):
            self.logger.warning(
                "Monitor service is already running, not starting again"
            )
            return

        # Создаем и запускаем задачу мониторинга
        self._monitor_task = asyncio.create_task(self._run_monitoring())
        self.logger.info("Monitoring task created")

    async def _run_monitoring(self):
        """Запуск мониторинга"""
        try:
            self.logger.info("Starting monitoring in background")

            # Убедимся, что сервис в правильном состоянии
            if hasattr(self._monitor_service, "_running"):
                self._monitor_service._running = True

            # Запускаем мониторинг
            await self._monitor_service.run()
            self.logger.info("Monitoring completed or stopped normally")

        except asyncio.CancelledError:
            self.logger.info("Monitoring task was cancelled")

        except Exception as e:
            error_msg = f"Error in monitoring: {str(e)}\n{traceback.format_exc()}"
            self.logger.error(error_msg)

            # Обновляем статус
            self._monitoring_started = False
            self.update_monitor_status(self._monitoring_started)

    def _stop_monitoring(self):
        """Остановка мониторинга"""
        try:
            if self._monitor_service:
                self.logger.info("Stopping monitor service...")
                self._monitor_service.stop()

            if self._monitor_task and not self._monitor_task.done():
                self.logger.info("Cancelling monitor task...")
                self._monitor_task.cancel()

            self._monitoring_started = False
            self.update_monitor_status(self._monitoring_started)
            self.logger.info("Monitoring stopped")

        except Exception as e:
            error_msg = f"Error stopping monitoring: {str(e)}\n{traceback.format_exc()}"
            self.logger.error(error_msg)

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
                self._show_error_message("Интервал должен быть числом")
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
                    self._show_error_message("URL не может быть пустым")
                if interval <= 0:
                    interval_input.styles.border = ("solid", "red")
                    self._show_error_message("Интервал должен быть больше 0")

    def update_monitor_status(self, is_running: bool):
        try:
            self.logger.debug(f"Updating monitor status: is_running={is_running}")
            status_widget = self.query_one("#monitor_status", Static)
            if is_running:
                status_widget.update("Мониторинг: запущен ✓")
                status_widget.remove_class("status-stopped")
                status_widget.add_class("status-running")
                self.logger.debug("Monitor status updated to: running")
            else:
                status_widget.update("Мониторинг: остановлен ✗")
                status_widget.remove_class("status-running")
                status_widget.add_class("status-stopped")
                self.logger.debug("Monitor status updated to: stopped")
        except Exception as e:
            self.logger.error(f"Error updating monitor status: {e}")

    def on_unmount(self):
        """Вызывается при демонтировании экрана"""
        self.logger.info("MainScreen unmounting")
        self._stop_monitoring()

        # Закрываем обработчики логгера
        for handler in self.logger.handlers:
            try:
                handler.close()
            except:
                pass
        self.logger.info("MainScreen unmounted")

    def on_monitoring_table_monitor_row_selected(
        self, message: MonitoringTable.MonitorRowSelected
    ) -> None:
        monitor_id = message.row_id
        if monitor_id:
            self._row = monitor_id
