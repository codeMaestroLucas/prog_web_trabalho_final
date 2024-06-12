from pydantic import BaseModel
from typing import List

class Order(BaseModel):
    """Classe de Pedido.
    
    Herda de BaseModel e representa um pedido completo, incluindo a
    configuração para trabalhar com ORM - converte automaticamente dados de
    objetos ORM (Object-Relational Mapping) para modelos Pydantic."""
    # id: int
    user_id: int
    products: List[int]
    
    class Config:
        from_attributes  = True