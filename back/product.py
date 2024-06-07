from abc import ABC, abstractmethod

class Product:
    def __init__(self, name: str, price: float, quantity: int) -> None:
        self._name = name.tile().strip()
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
        
if __name__ == '__main__':
    ...