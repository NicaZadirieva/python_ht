from collections import deque
from datetime import datetime
from typing import Optional
import time

from textual_app.domain import MonitorData


class MonitorService:
    _last_checked_time: datetime = datetime.now()
    waiting_queue: deque[MonitorData] = deque()

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

    def run(self):
        """
        Запуск бесконечного мониторинга
        """
        while True:
            try:
                if self.waiting_queue:
                    first_item = self.waiting_queue.popleft()
                    current_time = datetime.now()

                    # Проверяем, пора ли проверять этот элемент
                    should_check = False

                    if (
                        first_item.latest_checked_time is None
                        and (current_time - self._last_checked_time).total_seconds()
                        >= first_item.interval
                    ):
                        # Если никогда не проверяли - проверяем сразу
                        should_check = True
                    elif first_item.latest_checked_time:
                        # Если проверяли ранее, смотрим, прошло ли достаточно времени
                        time_since_last_check = (
                            current_time - first_item.latest_checked_time
                        ).total_seconds()
                        if time_since_last_check >= first_item.interval:
                            should_check = True

                    if should_check:
                        self._last_checked_time = current_time
                        first_item.latest_checked_time = self._last_checked_time

                        # Здесь должна быть логика фактической проверки (пинга)
                        # Например: self._perform_ping(first_item)

                        print(f"Проверка элемента {first_item.id} в {current_time}")

                    # Возвращаем элемент обратно в очередь
                    self.add(first_item)

            except KeyboardInterrupt:
                # Позволяет корректно завершить программу по Ctrl+C
                print("Мониторинг остановлен")
                break
            except Exception as e:
                # Логируем ошибки, но продолжаем работу
                print(f"Ошибка при выполнении мониторинга: {e}")
