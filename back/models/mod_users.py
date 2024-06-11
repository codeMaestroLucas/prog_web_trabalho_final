from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """Classe de Usuário
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable= False)
    name = Column(String, nullable= False)
    email = Column(String, unique=True, nullable= False)
    password = Column(String, nullable= False)
    
    order_id = Column(Integer, ForeignKey("orders.id"))