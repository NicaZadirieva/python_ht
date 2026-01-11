"""
У нас есть отель, в котором есть номера разных типов (от Room):

Обычный номер
Люкс (имеет мультипликатор цены)
Гость может:

бронировать номер на определённые даты - через класс Booking - бронирование. Его можно отменить.
Отель (класс Hotel) должен:

уметь показывать список доступных номеров на заданные даты;
добавить номер
забронировать и отменить бронирование
показать забронированные номера
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
@dataclass
class Room(ABC):
    price: float
    not_available_from: datetime = None
    not_available_to: datetime = None
    room_number: int

    """Общий класс номера в отеле"""
    @abstractmethod
    def get_price(self) -> float:
        """Получение цены номера в отеле"""
        pass

    def cancel_order(self):
        self.not_available_from = None
        self.not_available_to = None
        return self

    def book_room(self, not_available_from: datetime = None, not_available_to: datetime = None):
        self.not_available_from = not_available_from
        self.not_available_to = not_available_to
        return self



@dataclass
class LuxaryRoom(Room):
    """Номер люкс"""

    """Мультипликатор цены"""
    multiplicator: float
    def get_price(self) -> float:
        return self.price * self.multiplicator


@dataclass
class SimpleRoom(Room):
    """Обычный номер"""

    def get_price(self) -> float:
        return self.price


class Booking:
    def create_room(self, price: float, room_number: int, multiplicator: float = None):
        if multiplicator is None:
            # создаем обычный номер
            return SimpleRoom(price, room_number)
        else:
            # создаем номер люкс
            return LuxaryRoom(price, room_number, multiplicator)

    def book_room(self, room: Room, not_available_from: datetime, not_available_to: datetime):
        return room.book_room(not_available_from, not_available_to)

    def cancel_order(self, room: Room):
        return room.cancel_order()

@dataclass
class Hotel:
    bookingService: Booking
    available_rooms_for_ordering: list[Room] = []
    booked_rooms: list[Room] = []

    def show_all_available_rooms(self, date_to_order: datetime):
        for room in self.available_rooms_for_ordering:
            if room.not_available_from > date_to_order > room.not_available_to:
                print(room)

    def show_all_booked_rooms(self):
        for room in self.booked_rooms:
            print(room)

    def add_room(self, price: float, room_number: int, multiplicator: float = None):
        room = self.bookingService.create_room(price, room_number, multiplicator)
        self.available_rooms_for_ordering.append(room)
        return room

    def __get_room__(self, storage: list[Room], room_number: int):
        for room in storage:
            if room.room_number == room_number:
                return room
        return None

    def book_room(self, room_number: int, not_available_from: datetime, not_available_to: datetime):
        if self.__get_room__(self.booked_rooms, room_number):
            raise ValueError("Нельзя забронировать уже забронированный номер")
        old_room = self.__get_room__(self.available_rooms_for_ordering, room_number)
        if old_room is None:
            raise ValueError("Такого номера не существует")
        booked_room = self.bookingService.book_room(old_room, not_available_from, not_available_to)
        self.booked_rooms.append(booked_room)
        return booked_room

    def cancel_room(self, room_number: int):
        if self.__get_room__(self.available_rooms_for_ordering, room_number):
            raise ValueError("Нельзя отменить уже отмененный номер")
        old_room = self.__get_room__(self.booked_rooms, room_number)
        if old_room is None:
            raise ValueError("Такого номера не существует")
        cancelled_room = self.bookingService.cancel_order(old_room)
        self.available_rooms_for_ordering.append(cancelled_room)
        return cancelled_room
