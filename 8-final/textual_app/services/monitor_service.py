from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import asyncio
import signal

from textual_app.domain import MonitorData


@dataclass
class MonitorService:
    _last_checked_time: datetime = datetime.now()
    waiting_queue: deque[MonitorData] = field(default_factory=deque)

    def add(self, item: MonitorData) -> MonitorData:
        """
        Добавление данных для мониторинга
        """
        candidate: Optional[MonitorData] = None
        for monitor in self.waiting_queue:
            if candidate is None or item.is_after(monitor):
                candidate = monitor
        if candidate:
            self.waiting_queue.insert(candidate.id + 1, item)
        else:
            self.waiting_queue.append(item)
        return item

    async def run(self):
        """
        Асинхронный запуск бесконечного мониторинга
        """
        # Обработка Ctrl+C для graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self.stop)

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
                        self._last_checked_time = current_time
                        item.latest_checked_time = current_time
                        items_to_check.append(item)

                # Асинхронно проверяем все элементы, которые нужно проверить
                if items_to_check:
                    tasks = [self._perform_async_check(item) for item in items_to_check]
                    await asyncio.gather(*tasks, return_exceptions=True)

                # Даем возможность другим задачам выполняться
                await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                print("Мониторинг остановлен по запросу отмены")
                break
            except Exception as e:
                # Логируем ошибки, но продолжаем работу
                print(f"Ошибка при выполнении мониторинга: {e}")
                await asyncio.sleep(1)  # Пауза при ошибке

    def stop(self):
        """Остановка мониторинга"""
        self._running = False

    async def _perform_async_check(self, item):
        """
        Асинхронная проверка элемента (заглушка для реальной логики)
        """
        try:
            # Здесь должна быть асинхронная логика фактической проверки
            # Например: await self._async_ping(item)
            print(f"Асинхронная проверка элемента {item.id} в {datetime.now()}")

            # Имитация асинхронной работы
            await asyncio.sleep(0.01)

        except Exception as e:
            print(f"Ошибка при проверке элемента {item.id}: {e}")

    async def run_with_timeout(self, timeout=None):
        """
        Запуск мониторинга с возможностью таймаута
        """
        try:
            if timeout:
                await asyncio.wait_for(self.run(), timeout)
            else:
                await self.run()
        except asyncio.TimeoutError:
            print(f"Мониторинг остановлен по таймауту ({timeout} сек)")
        finally:
            self.stop()
