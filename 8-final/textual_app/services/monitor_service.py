from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from types import CoroutineType
from typing import Optional
import asyncio
import signal
import logging
from logging.handlers import RotatingFileHandler
import sys
import aiohttp
import ssl

from textual_app.domain import MonitorData, HttpStatus
from textual_app.repositories import BaseMonitorDataRepository


@dataclass
class MonitorService:
    _monitor_data_repo: BaseMonitorDataRepository
    _last_checked_time: datetime = datetime.now()
    waiting_queue: deque[MonitorData] = field(default_factory=deque)
    mapping_tasks: dict[int, Optional[CoroutineType]] = field(default_factory=dict)
    _running: bool = True
    _logger: logging.Logger = field(init=False)
    _session: Optional[aiohttp.ClientSession] = None
    _timeout: int = 10  # Таймаут по умолчанию 10 секунд
    _max_retries: int = 3  # Максимальное количество попыток
    _verify_ssl: bool = True  # Проверять SSL сертификаты

    def delete_by_monitor_id(self, monitor_id: int):
        """
        Удаление задачи по id-ку строки
        """
        task = self.mapping_tasks[monitor_id]
        if task:
            try:
                task.throw(asyncio.CancelledError)
            except:  # noqa: E722
                self._logger.info(f"Task for row#{monitor_id} is stopped")
            self.mapping_tasks[monitor_id] = None
            monitor_to_delete = None
            for monitor in self.waiting_queue:
                if monitor.id == monitor_id:
                    monitor_to_delete = monitor
            if monitor_to_delete:
                self.waiting_queue.remove(monitor_to_delete)

    def __post_init__(self):
        """Инициализация логгера после создания экземпляра класса"""
        self._logger = self._setup_logger()

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

    def add(self, item: MonitorData) -> MonitorData:
        """
        Добавление данных для мониторинга
        """
        self._logger.debug(f"Добавление элемента мониторинга: {item}")
        candidate: Optional[MonitorData] = None
        for monitor in self.waiting_queue:
            if candidate is None or item.is_after(monitor):
                candidate = monitor
        if candidate:
            self.waiting_queue.insert(candidate.id + 1, item)
            self._logger.info(
                f"Элемент {item.id} добавлен в позицию {candidate.id + 1}"
            )
        else:
            self.waiting_queue.append(item)
            self._logger.info(f"Элемент {item.id} добавлен в конец очереди")

        self._logger.debug(f"Текущий размер очереди: {len(self.waiting_queue)}")
        return item

    async def run(self):
        """
        Асинхронный запуск бесконечного мониторинга
        """
        self._logger.info("Запуск мониторинга")

        # Обработка Ctrl+C для graceful shutdown
        try:
            loop = asyncio.get_running_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, self.stop)
        except (NotImplementedError, RuntimeError):
            # Не поддерживается на текущей платформе или loop не запущен
            pass

        self._logger.debug("Сигнальные обработчики установлены")

        while self._running:
            try:
                # Создаем копию элементов для проверки, чтобы избежать модификации во время итерации
                items_to_check = []

                # Проверяем все элементы в очереди
                for item in list(self.waiting_queue):
                    current_time = datetime.now()
                    should_check = False

                    if (
                        item.latest_checked_time is None
                        and (
                            current_time - (self._last_checked_time or current_time)
                        ).total_seconds()
                        >= item.interval
                    ):
                        # Если никогда не проверяли - проверяем
                        should_check = True
                    elif item.latest_checked_time:
                        # Если проверяли ранее, смотрим, прошло ли достаточно времени
                        time_since_last_check = (
                            current_time - item.latest_checked_time
                        ).total_seconds()
                        if time_since_last_check >= item.interval:
                            should_check = True

                    if should_check:
                        self._logger.debug(f"Элемент {item.id} готов к проверке")
                        self._last_checked_time = current_time
                        item.latest_checked_time = current_time
                        items_to_check.append(item)

                # Асинхронно проверяем все элементы, которые нужно проверить
                if items_to_check:
                    self._logger.info(
                        f"Начинаем проверку {len(items_to_check)} элементов"
                    )
                    tasks = []
                    for item in items_to_check:
                        task = self._perform_async_check(item)
                        self.mapping_tasks[item.id] = task
                        tasks.append(task)

                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    # Логируем результаты проверки
                    for item, result in zip(items_to_check, results):
                        if isinstance(result, Exception):
                            self._logger.error(
                                f"Ошибка при проверке элемента {item.id}: {result}"
                            )
                        else:
                            self._logger.debug(f"Элемент {item.id} успешно проверен")

                # Даем возможность другим задачам выполняться
                await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                self._logger.warning("Мониторинг остановлен по запросу отмены")
                break
            except Exception as e:
                # Логируем ошибки, но продолжаем работу
                self._logger.error(
                    f"Ошибка при выполнении мониторинга: {e}", exc_info=True
                )
                await asyncio.sleep(1)  # Пауза при ошибке

        self._logger.info("Мониторинг остановлен")

    def stop(self):
        """Остановка мониторинга"""
        self._logger.info("Получен сигнал на остановку мониторинга")
        self._running = False

    async def _create_session(self):
        """Создание aiohttp сессии"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            connector = aiohttp.TCPConnector(
                ssl=ssl.create_default_context() if self._verify_ssl else False,
                limit=100,  # Максимальное количество соединений
                limit_per_host=10,  # Максимальное количество соединений на хост
            )

            self._session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={"User-Agent": "MonitorService/1.0", "Accept": "*/*"},
            )
            self._logger.debug("Сессия aiohttp создана")

    async def _perform_async_check(self, item: MonitorData):
        """
        Асинхронная проверка HTTP доступности URL
        """
        try:
            # Создаем сессию, если её нет
            await self._create_session()

            self._logger.debug(f"Начало проверки URL: {item.url} (ID: {item.id})")

            start_time = datetime.now()

            # Выполняем HTTP запрос с повторными попытками
            response = None
            last_exception = None

            for attempt in range(self._max_retries):
                try:
                    self._logger.debug(
                        f"Попытка {attempt + 1}/{self._max_retries} для {item.url}"
                    )

                    async with self._session.get(  # type: ignore
                        item.url,
                        allow_redirects=True,
                        ssl=False
                        if not self._verify_ssl
                        else ssl.create_default_context(),
                    ) as resp:
                        response = resp

                        # Читаем небольшой кусок тела для проверки доступности контента
                        await resp.read()

                        # Если успешно - прерываем цикл повторных попыток
                        break

                except aiohttp.ClientTimeoutError as e:
                    last_exception = e
                    self._logger.warning(
                        f"Таймаут при попытке {attempt + 1} для {item.url}: {e}"
                    )
                    if attempt < self._max_retries - 1:
                        await asyncio.sleep(2**attempt)  # Экспоненциальная задержка
                    continue

                except aiohttp.ClientConnectorSSLError as e:
                    last_exception = e
                    self._logger.error(f"SSL ошибка для {item.url}: {e}")
                    item.status = HttpStatus.FAILED
                    break

                except aiohttp.ClientConnectorError as e:
                    last_exception = e
                    self._logger.error(f"Ошибка подключения для {item.url}: {e}")
                    item.status = HttpStatus.FAILED
                    if attempt < self._max_retries - 1:
                        await asyncio.sleep(2**attempt)
                    continue

                except Exception as e:
                    last_exception = e
                    self._logger.error(f"Неожиданная ошибка для {item.url}: {e}")
                    if attempt < self._max_retries - 1:
                        await asyncio.sleep(2**attempt)
                    continue

            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000  # мс

            # Обрабатываем результат
            if response:
                # Обновляем данные мониторинга
                item.http_code = response.status
                item.latest_checked_time = datetime.now()  # Время проверки

                # Определяем статус на основе кода ответа
                if 200 <= response.status < 300:
                    item.status = HttpStatus.OK
                    self._logger.info(
                        f"URL {item.url} доступен. Код: {response.status}, "
                        f"Время ответа: {response_time:.2f}мс"
                    )
                elif 300 <= response.status < 400:
                    item.status = HttpStatus.FAILED  # Редиректы считаем доступными
                    self._logger.warning(
                        f"URL {item.url} редирект. Код: {response.status}"
                    )
                else:
                    item.status = HttpStatus.FAILED
                    self._logger.error(
                        f"URL {item.url} недоступен. Код: {response.status}"
                    )

            else:
                # Не удалось получить ответ после всех попыток
                item.http_code = None
                item.status = HttpStatus.FAILED if not item.status else item.status
                item.latest_checked_time = datetime.now()

                if isinstance(last_exception, aiohttp.ClientTimeoutError):
                    item.status = HttpStatus.FAILED
                    self._logger.error(
                        f"Таймаут для URL {item.url} после {self._max_retries} попыток"
                    )
                else:
                    self._logger.error(
                        f"Не удалось проверить URL {item.url}: {last_exception}"
                    )

            self._logger.debug(f"Завершение проверки URL: {item.url}")
            # После проверки обновляем элемент в репозитории
            if hasattr(self, "_monitor_data_repo"):
                self._monitor_data_repo.update_by_id(item.id, item)

            self._logger.info(
                f"Checked {item.url}: "
                f"Status={item.status.value if item.status else 'UNKNOWN'}, "
                f"Code={item.http_code}, "
                f"ResponseTime={item.latest_checked_time}ms"
            )
            return True

        except asyncio.CancelledError:
            self._logger.warning(f"Проверка URL {item.url} была отменена")
            raise

        except Exception as e:
            self._logger.error(
                f"Критическая ошибка при проверке URL {item.url}: {e}", exc_info=True
            )

            # Устанавливаем статус неизвестно в случае непредвиденной ошибки
            item.http_code = None
            item.status = HttpStatus.UNKNOWN
            item.latest_checked_time = datetime.now()
            raise

    async def run_with_timeout(self, timeout=None):
        """
        Запуск мониторинга с возможностью таймаута
        """
        self._logger.info(
            f"Запуск мониторинга с таймаутом: {timeout} сек"
            if timeout
            else "Запуск мониторинга без таймаута"
        )

        try:
            if timeout:
                await asyncio.wait_for(self.run(), timeout)
            else:
                await self.run()
        except asyncio.TimeoutError:
            self._logger.warning(f"Мониторинг остановлен по таймауту ({timeout} сек)")
        except Exception as e:
            self._logger.error(f"Неожиданная ошибка при работе мониторинга: {e}")
        finally:
            self.stop()

    def set_log_level(self, level: str):
        """Установка уровня логирования"""
        level_mapping = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        if level.upper() in level_mapping:
            self._logger.setLevel(level_mapping[level.upper()])
            for handler in self._logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(level_mapping[level.upper()])
            self._logger.info(f"Уровень логирования изменен на {level}")
        else:
            self._logger.warning(f"Неизвестный уровень логирования: {level}")
