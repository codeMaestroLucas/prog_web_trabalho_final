from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    """Classe de Usuário.
    
    Estabelece uma estrutura que será usada no Banco de Dados.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String)
    email = Column(String, unique= True)
    password = Column(String)