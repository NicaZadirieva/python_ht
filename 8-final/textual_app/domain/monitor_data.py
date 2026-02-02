"""
Бизнес-сущность "Данные мониторинга"
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from textual_app.domain.status import Status


@dataclass
class MonitorData:
    """
    Данные мониторинга (одна строка таблицы)
    """

    id: int
    url: str
    interval: int
    status: Optional[Status]
    http_code: Optional[int]
    latest_checked_time: Optional[datetime]

    def is_after(self, item: "MonitorData") -> bool:
        """
        True, если мониторинг должен произойти позже item
        """
        current_monitor_check_secs = (
            0 if self.latest_checked_time is None else self.latest_checked_time.second
        )
        item_check_secs = (
            0 if item.latest_checked_time is None else item.latest_checked_time.second
        )
        return (
            current_monitor_check_secs + self.interval > item_check_secs + item.interval
        )
