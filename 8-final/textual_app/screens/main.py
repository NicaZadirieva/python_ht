"""
Основной экран
"""

from textual.events import Mount
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input
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

        # Подписываемся на обновления сервиса мониторинга
        self._setup_monitoring_updates()

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
        # Создаем таблицу с колбэком для обновления
        yield MonitoringTable(
            self._monitor_data_repo, on_data_change=self._on_table_data_change
        )

        yield Footer()

    def _on_mount(self, event: Mount) -> None:
        """
        Монтирование
        """
        self.title = "Менеджер проверки доступа URL"

        # Запускаем периодическое обновление таблицы
        self.set_interval(1, self._refresh_table)

    def _setup_monitoring_updates(self):
        """Настройка получения обновлений от сервиса мониторинга"""
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
                    monitor_table.update_table()
        except Exception as e:
            # Игнорируем ошибки при обновлении, чтобы не падало приложение
            pass

    def _on_table_data_change(self):
        """Колбэк при изменении данных в таблице"""
        self._refresh_table()

    def action_quit(self):
        """
        Выход из приложения
        """
        self.app.exit()

    def add_new_monitor_data(self, url: str, interval: int):
        """Добавление новых данных для мониторинга"""
        try:
            # Определяем следующий ID
            existing_items = self._monitor_data_repo.load()
            next_id = max([item.id for item in existing_items], default=0) + 1

            item = MonitorData(
                id=next_id, url=url, interval=interval, status=HttpStatus.PENDING
            )

            # Добавляем в репозиторий
            added_item = self._monitor_data_repo.add_item(item)

            # Добавляем в сервис мониторинга
            self._monitor_service.add(added_item)

            # Обновляем таблицу
            monitor_table = self.query_one(MonitoringTable)
            monitor_table.update_table()

            # Если мониторинг еще не запущен, запускаем его
            if not self._monitoring_started:
                self._start_monitoring()
                self._monitoring_started = True

        except Exception as e:
            # Обработка ошибок при добавлении
            print(f"Ошибка при добавлении данных мониторинга: {e}")

    @work
    async def _start_monitoring(self):
        """Запуск мониторинга в фоновом режиме"""
        try:
            # Запускаем мониторинг в фоновом режиме
            await self._monitor_service.run()
        except Exception as e:
            print(f"Ошибка при запуске мониторинга: {e}")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_btn":
            url_input = self.query_one("#input_url", Input)
            url = url_input.value.strip()
            interval_input = self.query_one("#input_interval", Input)

            try:
                interval = int(interval_input.value.strip())
            except ValueError:
                # Невалидный интервал
                interval_input.styles.border = ("solid", "red")
                return

            if url and interval > 0:
                self.add_new_monitor_data(url, interval)

                # Сбрасываем поля ввода
                url_input.value = ""
                interval_input.value = ""
                url_input.styles.border = ("none", "white")
                interval_input.styles.border = ("none", "white")
            else:
                # Подсвечиваем невалидные поля
                if not url:
                    url_input.styles.border = ("solid", "red")
                if interval <= 0:
                    interval_input.styles.border = ("solid", "red")
