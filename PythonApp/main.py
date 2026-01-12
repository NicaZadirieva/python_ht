"""Принцип открытости-закрытости"""
"""Классы должны быть открыты для расширения, но закрыты для модификации."""

class Notifier:
    def send(self, message: str, method: str) -> None:
        if method == "email":
            print(f"[Email] Отправлено сообщение: {message}")
        elif method == "push":
            print(f"[Push] Отправлено сообщение: {message}")
        else:
            print("Неизвестный способ уведомления")
