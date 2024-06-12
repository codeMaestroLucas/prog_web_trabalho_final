from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
    
order_products = Table(
    'order_products', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

class Order(Base):
    """Classe de Pedidos
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key= True, autoincrement= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    products = relationship('Product', secondary=order_products, back_populates='orders')