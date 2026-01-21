def safe_div(a: float, b: float) -> float | str:
    if b == 0:
        return "деление на ноль"
    return a / b

def ensure_list(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return value
    return [value]