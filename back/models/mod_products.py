from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    """Classe de Produtos
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable= False)
    name = Column(String, nullable= False)
    price = Column(Float, nullable= False)
    quantity = Column(Integer, nullable= False)
    
    order_id = Column(Integer, ForeignKey("orders.id"))