from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import mod_products
from schemas import sch_products
import database

router = APIRouter()

@router.post("/products/", response_model= sch_products.Product)
def create_product(product: sch_products.Product,
                   db: Session= Depends(database.get_db)) -> mod_products.Product:
    """Função usada para criar um novo produto.

    Args:
        product (sch_products.Product): Produto que será criado.
        db (Session, optional): Sessão do banco de dados usada para enviar os
        dados. Defaults to Depends(database.get_db).

    Returns:
        mod_products.Product: O produto criado.
    """
    
    db_product = mod_products.Product(name= product.name,
                                         price= product.price,
                                         quantity= product.quantity)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


@router.get("/products/{product_id}", response_model= sch_products.Product)
def get_product(product_id: int, db: Session= Depends(database.get_db)) -> mod_products.Product:
    """Função usada para retornar produtos que já foram criados.

    Args:
        product_id (int): id do produto.
        db (Session, optional): Sessão do banco de dados que será usada para
        enviar os dados. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: caso não haja um id correspondente ao que foi solicitado.

    Returns:
        mod_products.Product: produto correspondente ao id solicitado.
    """
    db_product = db.query(mod_products.Product).filter(mod_products.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code= 404, detail= "Produto não encontrado.")
        
    return db_product