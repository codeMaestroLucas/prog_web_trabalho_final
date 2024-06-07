from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name: str, email: str, password: str) -> None:
        self._name = name.title().strip()
        self._email = email.strip().replace(" ", "")
        self._password = password.strip().replace(" ", "")
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = password

class Client(Person): ...


if __name__ == '__main__':
    c1 = Client('lucas samuel', '   lu  cas@e   mail  ', '    hdb  visdf v '  )
    print(c1.__dict__)