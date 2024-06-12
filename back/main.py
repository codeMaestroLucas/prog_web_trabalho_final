from typing import Tuple
from fastapi import FastAPI, APIRouter
from routes import rt_products, rt_users, rt_orders
from database import engine, Base
import uvicorn


def add_routes(app: FastAPI):
    """Função usada para adicionar as rotas inseridas na tupla "routes".

    Args:
        app (FastAPI): app que será usado para receber as rotas.

    Returns:
        Retorna o app com as rotas adicionadas.
    """
    routes: Tuple[APIRouter] = (rt_products.router,
                                rt_users.router,
                                rt_orders.router)

    for route in routes:
        app.include_router(route)
        
    return app
        
def main() -> None:
    """Função usada para rodar o código principal."""

    Base.metadata.create_all(bind= engine)

    app = FastAPI()

    add_routes(app)
    uvicorn.run(app)


if __name__ == '__main__':
    main()