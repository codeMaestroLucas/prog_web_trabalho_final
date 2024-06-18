from ..database import Base
from sqlalchemy import Column, String, Integer, Float

class Product(Base):
    """Classe de Produtos.
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String)
    price = Column(Float)
    in_stock = Column(Integer)