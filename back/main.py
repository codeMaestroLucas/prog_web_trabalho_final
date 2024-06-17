from typing import Tuple
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from routes import rt_products, rt_users, rt_orders
from database import Base, engine
from uvicorn import run

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Função usada para iniciar o DB."""
    Base.metadata.create_all(bind= engine)
    yield

def add_routes(app: FastAPI):
    """Função usada para adicionar os endpoints no APP."""
    routes: Tuple[APIRouter] = (
        rt_users.router,
        rt_products.router,
        rt_orders.router
    )

    for route in routes:
        app.include_router(route)


app = FastAPI(
    title='Trabalho Final ProgWeb',
    description='API de gerenciamento de uma pizzaria.',
    lifespan= lifespan
)

add_routes(app)
run(app)