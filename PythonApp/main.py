"""Interface Segregation Principle"""

"""
Программисты не должны заставлять классы имплементировать методы, которые им не требуются. 
Интерфейсы должны быть узкими и специализированными, чтобы избежать ненужной функциональности.
"""

# class PaymentProcessor:
#     def pay(self, amount: float):
#         pass

#     def refund(self, amount: float):
#         pass

#     def tokenize_card(self, card_number: str):
#         pass

#     def check_balance(self):
#         pass

from abc import ABC, abstractmethod

class Payable(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class Refundable(ABC):
    @abstractmethod
    def refund(self, amount: float):
        pass

class Tokenizable(ABC):
    @abstractmethod
    def tokenize_card(self, card_number: str):
         pass

class BalanceCheckable(ABC):
    @abstractmethod
    def check_balance(self):
         pass



class MasterCard(Payable, Tokenizable):
    def pay(self, amount: float):
        pass
   
    def tokenize_card(self, card_number: str):
         pass
   
class PayPal(Payable, BalanceCheckable):
    def pay(self, amount: float):
        pass
    def check_balance(self):
         pass

class Kiwi(Payable, Refundable):
    def pay(self, amount: float):
        pass
    def refund(self, amount: float):
        pass