"""
Тип статус
"""

from typing import Literal


# Статус запроса
type Status = Literal["OK", "Pending", "Failed"]
