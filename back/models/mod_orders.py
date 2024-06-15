from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Float

class Order(Base):
    """Classe de Pedidos
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key= True, autoincrement= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    total_value = Column(Float, default= 0)