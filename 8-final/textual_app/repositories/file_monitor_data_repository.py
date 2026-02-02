"""
Хранение результатов мониторинга в файле
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Union
import csv
from dataclasses import replace

from textual_app.domain import MonitorData
from textual_app.domain.status import HttpStatus
from textual_app.repositories.base_monitor_data_repository import (
    BaseMonitorDataRepository,
)


class FileMonitorDataRepository(BaseMonitorDataRepository):
    """
    Реализация работы с данными мониторинга через сохранение в файл
    """

    def __init__(self, file_path: Path | str) -> None:
        # путь до файла для сохранения
        self.file_path = Path(file_path).resolve()

        # Создаем файл, если его нет
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создает файл, если он не существует"""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            # Создаем файл с заголовками
            with open(self.file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "id",
                        "url",
                        "interval",
                        "status",
                        "http_code",
                        "latest_checked_time",
                    ]
                )

    def load(self) -> list[MonitorData]:
        """
        Загрузка данных мониторинга из CSV файла
        """
        monitor_data_list = []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)

                # Пропускаем заголовок
                next(reader, None)

                for row_num, row in enumerate(
                    reader, start=2
                ):  # start=2 так как первая строка - заголовок
                    try:
                        # Проверяем, что строка имеет правильное количество полей
                        if len(row) != 6:
                            print(
                                f"Предупреждение: строка {row_num} содержит {len(row)} полей вместо 6. Пропускаем."
                            )
                            continue

                        # Парсим поля
                        id_str = row[0].strip()
                        url = row[1].strip()
                        interval_str = row[2].strip()
                        status_str = row[3].strip()
                        http_code_str = row[4].strip()
                        datetime_str = row[5].strip()

                        # Преобразуем id
                        try:
                            monitor_id = int(id_str)
                        except ValueError:
                            print(
                                f"Ошибка в строке {row_num}: id '{id_str}' не является числом"
                            )
                            continue

                        # Преобразуем interval
                        try:
                            interval = int(interval_str)
                            if interval <= 0:
                                print(
                                    f"Ошибка в строке {row_num}: интервал должен быть положительным числом"
                                )
                                continue
                        except ValueError:
                            print(
                                f"Ошибка в строке {row_num}: интервал '{interval_str}' не является числом"
                            )
                            continue

                        # Преобразуем status (может быть пустым)
                        status: Optional[HttpStatus] = None
                        if status_str:
                            try:
                                # Пробуем получить значение Enum по строке
                                status = HttpStatus[status_str.upper()]
                            except KeyError:
                                # Если нет такого значения в Enum, создаем UNKNOWN
                                print(
                                    f"Предупреждение в строке {row_num}: неизвестный статус '{status_str}', устанавливаем UNKNOWN"
                                )
                                status = HttpStatus.UNKNOWN

                        # Преобразуем http_code (может быть пустым)
                        http_code = None
                        if http_code_str:
                            try:
                                http_code = int(http_code_str)
                            except ValueError:
                                print(
                                    f"Ошибка в строке {row_num}: http_code '{http_code_str}' не является числом"
                                )
                                continue

                        # Преобразуем latest_checked_time (может быть пустым)
                        latest_checked_time = None
                        if datetime_str:
                            try:
                                # Пробуем разные форматы даты
                                formats_to_try = [
                                    "%Y-%m-%d %H:%M:%S",
                                    "%Y-%m-%dT%H:%M:%S",
                                    "%d.%m.%Y %H:%M:%S",
                                    "%Y/%m/%d %H:%M:%S",
                                    "%Y-%m-%d %H:%M:%S.%f",  # С микросекундами
                                ]

                                for fmt in formats_to_try:
                                    try:
                                        latest_checked_time = datetime.strptime(
                                            datetime_str, fmt
                                        )
                                        break
                                    except ValueError:
                                        continue

                                if latest_checked_time is None:
                                    print(
                                        f"Предупреждение в строке {row_num}: не удалось распарсить дату '{datetime_str}'"
                                    )

                            except Exception as e:
                                print(
                                    f"Ошибка при парсинге даты в строке {row_num}: {e}"
                                )

                        # Создаем объект MonitorData
                        monitor_data = MonitorData(
                            id=monitor_id,
                            url=url,
                            interval=interval,
                            status=status,
                            http_code=http_code,
                            latest_checked_time=latest_checked_time,
                        )

                        monitor_data_list.append(monitor_data)

                    except Exception as e:
                        print(f"Ошибка при обработке строки {row_num}: {e}")
                        continue

        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден. Возвращаю пустой список.")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

        return monitor_data_list

    def _save_all(self, monitor_data_list: list[MonitorData]) -> None:
        """
        Сохраняет все данные в файл
        """
        try:
            # Сортируем по id для удобства чтения
            sorted_data = sorted(monitor_data_list, key=lambda x: x.id)

            with open(self.file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # Записываем заголовок
                writer.writerow(
                    [
                        "id",
                        "url",
                        "interval",
                        "status",
                        "http_code",
                        "latest_checked_time",
                    ]
                )

                for monitor_data in sorted_data:
                    # Преобразуем поля в строки
                    status_str = (
                        monitor_data.status.value if monitor_data.status else ""
                    )
                    http_code_str = (
                        str(monitor_data.http_code)
                        if monitor_data.http_code is not None
                        else ""
                    )

                    # Форматируем дату
                    datetime_str = ""
                    if monitor_data.latest_checked_time:
                        datetime_str = monitor_data.latest_checked_time.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                    writer.writerow(
                        [
                            str(monitor_data.id),
                            monitor_data.url,
                            str(monitor_data.interval),
                            status_str,
                            http_code_str,
                            datetime_str,
                        ]
                    )

        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")
            raise

    def delete(self, monitor_id: Union[int, str]) -> None:
        """
        Удаление данных по monitor_id
        """
        try:
            monitor_id_int = (
                int(monitor_id) if isinstance(monitor_id, str) else monitor_id
            )

            # Загружаем все данные
            all_data = self.load()

            # Фильтруем, оставляя только те, у которых id не равен заданному
            filtered_data = [item for item in all_data if item.id != monitor_id_int]

            # Сохраняем обновленные данные
            self._save_all(filtered_data)

        except ValueError:
            print(f"Ошибка: monitor_id '{monitor_id}' не является числом")
            raise
        except Exception as e:
            print(f"Ошибка при удалении записи: {e}")
            raise

    def add_item(self, item: MonitorData) -> MonitorData:
        """
        Добавление данных
        """
        try:
            # Загружаем все данные
            all_data = self.load()

            # Проверяем, существует ли уже запись с таким id
            if any(existing_item.id == item.id for existing_item in all_data):
                # Находим максимальный id и увеличиваем на 1
                max_id = (
                    max(existing_item.id for existing_item in all_data)
                    if all_data
                    else 0
                )
                new_id = max_id + 1

                # Создаем новую запись с новым id
                new_item = replace(item, id=new_id)
            else:
                new_item = item

            # Добавляем новую запись
            all_data.append(new_item)

            # Сохраняем все данные
            self._save_all(all_data)

            return new_item

        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")
            raise

    def update_by_id(
        self, monitor_id: Union[int, str], item: MonitorData
    ) -> MonitorData:
        """
        Обновление данных по id
        """
        try:
            monitor_id_int = (
                int(monitor_id) if isinstance(monitor_id, str) else monitor_id
            )

            # Загружаем все данные
            all_data = self.load()

            # Ищем запись с заданным id
            found_index = -1
            for i, existing_item in enumerate(all_data):
                if existing_item.id == monitor_id_int:
                    found_index = i
                    break

            if found_index == -1:
                raise ValueError(f"Запись с id {monitor_id_int} не найдена")

            # Создаем обновленную запись с сохранением оригинального id
            updated_item = replace(item, id=monitor_id_int)

            # Обновляем запись в списке
            all_data[found_index] = updated_item

            # Сохраняем все данные
            self._save_all(all_data)

            return updated_item

        except ValueError as e:
            print(f"Ошибка: {e}")
            raise
        except Exception as e:
            print(f"Ошибка при обновлении записи: {e}")
            raise

    def get_by_id(self, monitor_id: int) -> Optional[MonitorData]:
        """
        Получение данных по id
        """
        try:
            monitor_id_int = (
                int(monitor_id) if isinstance(monitor_id, str) else monitor_id
            )

            # Загружаем все данные
            all_data = self.load()

            # Ищем запись с заданным id
            for item in all_data:
                if item.id == monitor_id_int:
                    return item

            return None

        except ValueError:
            print(f"Ошибка: monitor_id '{monitor_id}' не является числом")
            return None
        except Exception as e:
            print(f"Ошибка при получении записи: {e}")
            return None
