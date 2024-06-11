from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import mod_users, mod_products, mod_orders
from schemas import sch_orders
import database

router = APIRouter()

@router.post("/orders/", response_model= sch_orders.Order)
def create_order(order: sch_orders.Order,
                 db: Session = Depends(database.get_db)):
    db_order = mod_orders.Order(user_id= order.user_id,
                                product_id= order.product_id)
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.get("/orders/{order_id}", response_model= sch_orders.Order)
def get_order(order_id: int, db: Session = Depends(database.get_db)):
    db_order = (db.query(mod_orders.Order)
            .join(mod_users.User, mod_orders.Order.user_id == mod_users.User.id)
            .join(mod_products.Product, mod_orders.Order.product_id == mod_products.Product.id)
            .filter(mod_orders.Order.id == order_id)
            .first())
    
    if not db_order:
        raise HTTPException(status_code= 404, detail= "Pedido não encontrado.")
        
    return db_order