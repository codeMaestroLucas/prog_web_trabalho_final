from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import mod_products
from schemas import sch_products
import database

router = APIRouter()

@router.post("/products/", response_model= sch_products.Product)
def create_product(product: sch_products.Product,
                   db: Session= Depends(database.get_db)):
    db_product = mod_products.Product(name= product.name,
                                         price= product.price,
                                         quantity= product.quantity)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


@router.get("/products/{product_id}", response_model= sch_products.Product)
def get_product(product_id: int, db: Session= Depends(database.get_db)):
    db_product = db.query(mod_products.Product).filter(mod_products.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code= 404, detail= "Produto não encontrado.")
        
    return db_product