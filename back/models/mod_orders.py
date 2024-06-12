from database import Base
<<<<<<< HEAD
from sqlalchemy import Column, Integer, ForeignKey
=======
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
    
order_products = Table(
    'order_products', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342

class Order(Base):
    """Classe de Pedidos
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key= True, autoincrement= True)
    user_id = Column(Integer, ForeignKey('users.id'))
<<<<<<< HEAD
    product_id = Column(Integer, ForeignKey('products.id'))
    
=======
    products = relationship('Product', secondary=order_products, back_populates='orders')
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342
