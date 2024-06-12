from database import Base
from sqlalchemy import Column, String, Integer, Float
<<<<<<< HEAD
=======
from sqlalchemy.orm import relationship
from mod_orders import order_products
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342

class Product(Base):
    """Classe de Produtos
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String)
    price = Column(Float)
<<<<<<< HEAD
    quantity = Column(Integer)
=======
    quantity = Column(Integer)

    orders = relationship('Order', secondary= order_products, back_populates= 'products')
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342
