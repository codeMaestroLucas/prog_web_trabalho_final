from typing import Tuple
from fastapi import FastAPI, APIRouter
from routes import rt_products, rt_users, rt_orders
from database import Base, engine
from contextlib import asynccontextmanager
from insert_data.send_data import insert_data
from uvicorn import run

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Função usada para iniciar o DB no momento da criação do APP.

    Args:
        app (FastAPI): APP que será criado.
    """
    Base.metadata.create_all(bind= engine)
    yield

def add_routes(app: FastAPI):
    """Função usada para adicionar as rotas inseridas na tupla "routes".

    Args:
        app (FastAPI): app que será usado para receber as rotas.

    Returns:
        Retorna o app com as rotas adicionadas.
    """
    routes: Tuple[APIRouter] = (
                                rt_users.router,
                                rt_products.router,
                                rt_orders.router)

    for route in routes:
        app.include_router(route)
        
    return app


def main() -> None:
    """Função usada para rodar o código principal."""
    app = FastAPI(lifespan= lifespan)

    add_routes(app)
    
    run(app)

if __name__ == '__main__':
    main()