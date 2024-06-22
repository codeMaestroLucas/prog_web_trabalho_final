from typing import Tuple
from fastapi import FastAPI, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from project.routes import rt_products, rt_users, rt_orders
from project.database import Base, engine, get_db
from project.models import mod_products, mod_orders

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
    app.mount('/static', StaticFiles(directory= 'project/static'), name= 'static')

    global templates
    templates = Jinja2Templates(directory= 'project/templates')

app = FastAPI(
    title= 'Trabalho Final ProgWeb',
    description= 'API de gerenciamento de uma pizzaria.',
    lifespan= lifespan
)

add_routes(app)
mount_app(app)


@app.get("/", response_class= HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}
        )

@app.get("/esqueceu", response_class= HTMLResponse)
async def esqueceu_senha(request: Request):
    return templates.TemplateResponse(
        "esqueceu.html", {"request": request}
        )

@app.get("/cadastro", response_class= HTMLResponse)
async def cadastro(request: Request):
    return templates.TemplateResponse(
        "cadastro.html", {"request": request}
        )

@app.get("/home", response_class= HTMLResponse)
async def home(request: Request, db: Session =  Depends(get_db)):
    
    products = db.query(mod_products.Product).all()
    orders = db.query(mod_orders.Order).all()
    
    
    return templates.TemplateResponse("home.html",
            {
                "request": request,
                "products": products,
                "orders": orders
             }
        )