from typing import Tuple
from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from project.routes import rt_products, rt_users, rt_orders
from project.database import Base, engine
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Função usada para iniciar o DB."""
    Base.metadata.create_all(bind= engine)
    #TODO: implementar Checagem se tabelas existem
    #TODO:
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

@app.get('/')
def home():
    return {'msg' : 'Hello World!'}

add_routes(app)