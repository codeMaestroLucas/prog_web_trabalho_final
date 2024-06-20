from typing import Tuple
from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from project.routes import rt_products, rt_users, rt_orders
from project.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Função usada para iniciar o DB."""
    Base.metadata.create_all(bind=engine)
    # TODO: implementar Checagem se tabelas existem
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

def mount_app(app: FastAPI):
    """Função usada para montar o APP com relação às pastas STATIC e TEMPLATES."""
    app.mount('/static', StaticFiles(directory='project/static'), name='static')

    global templates
    templates = Jinja2Templates(directory='project/templates')

app = FastAPI(
    title='Trabalho Final ProgWeb',
    description='API de gerenciamento de uma pizzaria.',
    lifespan=lifespan
)

add_routes(app)
mount_app(app)

@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request= request, name= 'login.html'
    )

@app.get("/esqueceu", response_class=HTMLResponse)
def esqueceu_senha(request: Request):
    return templates.TemplateResponse(
        request= request, name= 'esqueceu.html'
        )

@app.get("/cadastro", response_class=HTMLResponse)
def cadastro(request: Request):
    return templates.TemplateResponse(
        request= request, name= 'cadastro.html'
        )

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request= request, name= 'home.html'
        )