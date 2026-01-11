from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Room(ABC):
    """Общий класс номера в отеле"""
    price: float
    room_number: int
    
    @abstractmethod
    def get_price(self) -> float:
        """Получение цены номера в отеле"""
        pass


@dataclass
class LuxuryRoom(Room):
    """Номер люкс"""
    multiplicator: float
    
    def get_price(self) -> float:
        return self.price * self.multiplicator


@dataclass  
class SimpleRoom(Room):
    """Обычный номер"""
    
    def get_price(self) -> float:
        return self.price


@dataclass
class Reservation:
    """Класс для хранения информации о бронировании"""
    room: Room
    check_in: datetime
    check_out: datetime
    
    def dates_intersect(self, check_in: datetime, check_out: datetime) -> bool:
        """Проверяет, пересекаются ли даты с текущим бронированием"""
        return (self.check_in < check_out and self.check_out > check_in)


class BookingService:
    """Сервис для работы с бронированиями"""
    
    @staticmethod
    def create_room(price: float, room_number: int, multiplicator: float = None) -> Room:
        if multiplicator is None:
            return SimpleRoom(price, room_number)
        else:
            return LuxuryRoom(price, room_number, multiplicator)
    
    @staticmethod
    def dates_are_valid(check_in: datetime, check_out: datetime) -> bool:
        """Проверяет корректность дат бронирования"""
        if check_in >= check_out:
            return False
        if check_in < datetime.now():
            return False
        return True


@dataclass
class Hotel:
    """Класс отеля, управляет номерами и бронированиями"""
    booking_service: BookingService
    rooms: List[Room] = field(default_factory=list)
    reservations: List[Reservation] = field(default_factory=list)
    
    def _get_room_by_number(self, room_number: int) -> Optional[Room]:
        """Находит номер по номеру комнаты"""
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        return None
    
    def _is_room_available(self, room: Room, check_in: datetime, check_out: datetime) -> bool:
        """Проверяет, свободен ли номер на указанные даты"""
        for reservation in self.reservations:
            if reservation.room.room_number == room.room_number:
                if reservation.dates_intersect(check_in, check_out):
                    return False
        return True
    
    def add_room(self, price: float, room_number: int, multiplicator: float = None) -> Room:
        """Добавляет новый номер в отель"""
        # Проверяем, нет ли уже номера с таким номером
        if self._get_room_by_number(room_number):
            raise ValueError(f"Номер {room_number} уже существует")
        
        room = self.booking_service.create_room(price, room_number, multiplicator)
        self.rooms.append(room)
        return room
    
    def book_room(self, room_number: int, check_in: datetime, check_out: datetime) -> Reservation:
        """Бронирует номер на указанные даты"""
        # Проверяем корректность дат
        if not self.booking_service.dates_are_valid(check_in, check_out):
            raise ValueError("Некорректные даты бронирования")
        
        # Находим номер
        room = self._get_room_by_number(room_number)
        if room is None:
            raise ValueError(f"Номер {room_number} не найден")
        
        # Проверяем доступность номера на указанные даты
        if not self._is_room_available(room, check_in, check_out):
            raise ValueError(f"Номер {room_number} уже забронирован на указанные даты")
        
        # Создаем бронирование
        reservation = Reservation(room, check_in, check_out)
        self.reservations.append(reservation)
        return reservation
    
    def cancel_reservation(self, room_number: int, check_in: datetime, check_out: datetime) -> None:
        """Отменяет бронирование"""
        for i, reservation in enumerate(self.reservations):
            if (reservation.room.room_number == room_number and 
                reservation.check_in == check_in and 
                reservation.check_out == check_out):
                self.reservations.pop(i)
                return
        
        raise ValueError("Бронирование не найдено")
    
    def get_available_rooms(self, check_in: datetime, check_out: datetime) -> List[Room]:
        """Возвращает список доступных номеров на указанные даты"""
        if not self.booking_service.dates_are_valid(check_in, check_out):
            raise ValueError("Некорректные даты")
        
        available_rooms = []
        for room in self.rooms:
            if self._is_room_available(room, check_in, check_out):
                available_rooms.append(room)
        
        return available_rooms
    
    def show_available_rooms(self, check_in: datetime, check_out: datetime) -> None:
        """Показывает доступные номера на указанные даты"""
        available_rooms = self.get_available_rooms(check_in, check_out)
        
        if not available_rooms:
            print("Нет доступных номеров на указанные даты")
            return
        
        print(f"Доступные номера с {check_in} по {check_out}:")
        for room in available_rooms:
            room_type = "Люкс" if isinstance(room, LuxuryRoom) else "Обычный"
            print(f"  Номер {room.room_number}: {room_type}, цена: {room.get_price()}")
    
    def show_booked_rooms(self) -> None:
        """Показывает все текущие бронирования"""
        if not self.reservations:
            print("Нет активных бронирований")
            return
        
        print("Текущие бронирования:")
        for reservation in self.reservations:
            room = reservation.room
            room_type = "Люкс" if isinstance(room, LuxuryRoom) else "Обычный"
            print(f"  Номер {room.room_number} ({room_type}): "
                  f"с {reservation.check_in} по {reservation.check_out}, "
                  f"цена: {room.get_price()}")
    
    def get_room_reservations(self, room_number: int) -> List[Reservation]:
        """Возвращает все бронирования для указанного номера"""
        return [r for r in self.reservations if r.room.room_number == room_number]


# Пример использования
if __name__ == "__main__":
    # Создаем сервис бронирования и отель
    booking_service = BookingService()
    hotel = Hotel(booking_service)
    
    # Добавляем номера
    hotel.add_room(100.0, 101)  # Обычный номер
    hotel.add_room(200.0, 102, 1.5)  # Люкс с множителем 1.5
    hotel.add_room(150.0, 103)  # Еще один обычный номер
    
    # Создаем даты для бронирования
    from datetime import timedelta
    
    today = datetime.now()
    check_in1 = today + timedelta(days=1)
    check_out1 = today + timedelta(days=3)
    
    check_in2 = today + timedelta(days=4)
    check_out2 = today + timedelta(days=6)
    
    check_in3 = today + timedelta(days=2)  # Пересекается с первым бронированием
    check_out3 = today + timedelta(days=4)
    
    try:
        # Бронируем номер 101
        print("Бронируем номер 101 с", check_in1, "по", check_out1)
        hotel.book_room(101, check_in1, check_out1)
        
        # Пытаемся забронировать тот же номер на пересекающиеся даты
        print("\nПытаемся забронировать номер 101 с", check_in3, "по", check_out3)
        hotel.book_room(101, check_in3, check_out3)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Бронируем другой номер на непересекающиеся даты
    print("\nБронируем номер 102 с", check_in2, "по", check_out2)
    hotel.book_room(102, check_in2, check_out2)
    
    # Показываем доступные номера
    print("\n" + "="*50)
    hotel.show_available_rooms(check_in1, check_out1)
    
    print("\n" + "="*50)
    hotel.show_booked_rooms()
    
    # Отменяем бронирование
    print("\n" + "="*50)
    print("Отменяем бронирование номера 101")
    hotel.cancel_reservation(101, check_in1, check_out1)
    
    print("\n" + "="*50)
    hotel.show_available_rooms(check_in1, check_out1)