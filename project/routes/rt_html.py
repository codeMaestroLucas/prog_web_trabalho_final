from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.templating import Jinja2Templates
from ..utils.return_formatted_data import html_formatted


router = APIRouter(
    tags= ['HTMLs routes']
)

templates = Jinja2Templates(directory= 'project/templates')

@router.get("/", response_class= HTMLResponse)
async def login(request: Request) -> HTMLResponse:
    """Renderiza o "login.html" ao ser solicitado.

    Args:
        request (Request): Solicitação.

    Returns:
        HTMLResponse: Página de login.
    """
    return templates.TemplateResponse(
        "login.html", {"request": request}
        )

@router.get("/esqueceu", response_class= HTMLResponse)
async def esqueceu_senha(request: Request) -> HTMLResponse:
    """Renderiza o "esquece.html" ao ser solicitado.

    Args:
        request (Request): Solicitação.

    Returns:
        HTMLResponse: Página de "esqueceu a senha".
    """
    return templates.TemplateResponse(
        "esqueceu.html", {"request": request}
        )

@router.get("/cadastro", response_class= HTMLResponse)
async def cadastro(request: Request) -> HTMLResponse:
    """Renderiza o "cadastro.html" ao ser solicitado.

    Args:
        request (Request): Solicitação.

    Returns:
        HTMLResponse: Página de cadastro.
    """
    return templates.TemplateResponse(
        "cadastro.html", {"request": request}
        )

@router.get("/home", response_class= HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Renderiza o "cadastro.html" ao ser solicitado.

    Args:
        request (Request): Solicitação
        db (Session, optional): Conxão com o DB. Defaults to Depends(get_db).

    Returns:
        HTMLResponse: Página home.
    """
    formatted_products, formatted_orders = html_formatted(db)

    margin_top = (len(formatted_products) + len(formatted_orders)) * 100
    # Única maneira que achei de deixar responsivo. Será passada no style do main

    return templates.TemplateResponse("home_page/home.html", {
        "request": request,
        "products": formatted_products,
        "orders": formatted_orders,
        "margin_top": margin_top
    })

@router.get("/products/create", response_class= HTMLResponse)
async def create_products(request: Request,
                          db: Session = Depends(get_db)) -> HTMLResponse:
    """Renderiza o "create.html" ao ser solicitado.

    Args:
        request (Request): Solicitação
        db (Session, optional): Conxão com o DB. Defaults to Depends(get_db).

    Returns:
        HTMLResponse: Página home.
    """
    return templates.TemplateResponse("home_page/home_pop_ups/create.html", {
        "request": request})

@router.get("/products/update", response_class= HTMLResponse)
async def create_products(request: Request,
                          db: Session = Depends(get_db)) -> HTMLResponse:
    """Renderiza o "update.html" ao ser solicitado.

    Args:
        request (Request): Solicitação
        db (Session, optional): Conxão com o DB. Defaults to Depends(get_db).

    Returns:
        HTMLResponse: Página home.
    """
    return templates.TemplateResponse("home_page/home_pop_ups/update.html", {
        "request": request})