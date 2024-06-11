from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from mod_products import Product
from mod_users import User

Base = declarative_base()

class Order(Base):
    """Classe de Pedidos
    
    Estabelece uma estrutura que será usada no Banco de dados.
    """
    
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable= False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable= False)

    user = relationship(User)
    product = relationship(Product)
    