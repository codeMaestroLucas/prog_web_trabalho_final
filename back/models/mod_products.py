from database import Base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from mod_orders import order_products

class Product(Base):
    """Classe de Produtos
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    orders = relationship('Order', secondary= order_products, back_populates= 'products')