"""
Тип статус
"""

from enum import Enum


class HttpStatus(Enum):
    """
    Перечисление для статуса http-запроса
    """

    OK = "OK"
    PENDING = "Pending"
    FAILED = "Failed"
    UNKNOWN = "Unknown"
