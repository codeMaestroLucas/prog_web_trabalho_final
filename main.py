from typing import Tuple
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from project.routes import rt_products, rt_users, rt_orders, rt_html
from project.database import Base, engine

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
        rt_orders.router,
        rt_html.router
    )

    for route in routes:
        app.include_router(route)


app = FastAPI(
    title= 'Trabalho Final ProgWeb',
    description= 'API de gerenciamento de uma pizzaria.',
    lifespan= lifespan
)

app.mount('/static', StaticFiles(directory= 'project/static'), name= 'static')

add_routes(app)


import uvicorn

uvicorn.run(app)