from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, name: str, price: float, quantity: int) -> None:
        self._name = name.title().strip()
        self._price = price
        self._quantity = quantity
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity
    
    
    def __repr__(self):
        return f"""Product: {self.name}
Price = ${self.price:.2f}
Quantity = {self.quantity}"""
       
       
class Pizza(Product):
    def __init__(self, flavor: str, price: float, quantity: int) -> None:
        super().__init__(name='Pizza', price=price, quantity=quantity)
        self._flavor = flavor

if __name__ == '__main__':
    p1  = Pizza('peperonni', 40.31, 2)
    print(p1)