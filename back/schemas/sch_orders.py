from pydantic import BaseModel
<<<<<<< HEAD
=======
from typing import List
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342

class Order(BaseModel):
    """Classe de Pedido.
    
    Herda de BaseModel e representa um pedido completo, incluindo a
    configuração para trabalhar com ORM - converte automaticamente dados de
    objetos ORM (Object-Relational Mapping) para modelos Pydantic."""
    # id: int
    user_id: int
<<<<<<< HEAD
    product_id: int
=======
    products: List[int]
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342
    
    class Config:
        from_attributes  = True