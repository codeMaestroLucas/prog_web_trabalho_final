from products import Product

class Drink(Product):
    def __init__(self, name: str, price: float, quantity: int, liters: float) -> None:
        super().__init__(name=name, price=price, quantity=quantity)
        self._liters = liters

    @property
    def liters(self):
        return self._liters

    @liters.setter
    def liters(self, liters):
        self._liters = liters

    def __repr__(self):
        return f"""Drink: {self.name}
Price = ${self.price:.2f}
Quantity = {self.quantity}
Liters = {self.liters}L"""

class Soda(Drink):
    def __init__(self, name: str, price: float, quantity: int, liters: float) -> None:
        super().__init__(name=name, price=price, quantity=quantity, liters=liters)

if __name__ == '__main__':
    s1 = Soda('coke', 13.43, 5, 1.5)
    print(s1)
