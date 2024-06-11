from typing import Tuple
from fastapi import FastAPI, APIRouter
from routes import rt_products, rt_users
from database import engine, Base
import uvicorn
from models.mod_order import Base as OrderBase
from models.mod_products import Base as ProductBase
from models.mod_users import Base as UserBase

Base.metadata.create_all(bind= engine)


OrderBase.metadata.create_all(engine)
ProductBase.metadata.create_all(engine)
UserBase.metadata.create_all(engine)



app = FastAPI()

def add_routes(app: FastAPI):
    """Função usada para adicionar as rotas inseridas na tupla "routes".

    Args:
        app (FastAPI): app que será usado para receber as rotas.

    Returns:
        Retorna o app com as rotas adicionadas.
    """
    routes: Tuple[APIRouter] = (rt_products.router, rt_users.router)

    for route in routes:
        app.include_router(route)
        
    return app
        

add_routes(app)
uvicorn.run(app)