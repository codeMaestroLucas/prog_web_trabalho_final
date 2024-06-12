from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import mod_users, mod_products, mod_orders
from schemas import sch_orders
from models.mod_products import Product
import database

router = APIRouter()

@router.post("/orders/", response_model= sch_orders.Order)
def create_order(order: sch_orders.Order,
                 db: Session = Depends(database.get_db)) -> mod_orders.Order:
    """
    Função usada para se criar um novo pedido.

    Args:
        order (sch_orders.Order): Pedido que será criado.
        db (Session, optional): Sessão de banco de dados usada para enviar os
        dados. Defaults to Depends(database.get_db).

    Returns:
        mod_orders.Order: O pedido criado.
    """
    db_order = mod_orders.Order(user_id= order.user_id)
    
    # Adicione os produtos ao pedido
    for product_id in order.products:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db_order.products.append(product)
        else:
            raise HTTPException(status_code= 404, detail= "Produto não encontrado.")
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(database.get_db)) -> dict:
    """Função usada para retornar pedidos que já foram criados.

    Args:
        order_id (int): id do pedido.
        db (Session, optional): Sessão de banco de dados que será usada para
        enviar os dados. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: caso não haja um id correspondente ao que foi solicitado.

    Returns:
        dict: pedido correspondente ao id solicitado.
    """
    db_order = db.query(
        mod_orders.Order.id.label("order_id"),
        mod_users.User.name.label("user_name"),
        mod_products.Product.name.label("product_name"),
        mod_products.Product.price.label("product_price"),
        mod_products.Product.quantity.label("product_quantity")
    ).join(
        mod_users.User, mod_orders.Order.user_id == mod_users.User.id
    ).join(
        mod_products.Product, mod_orders.Order.product_id == mod_products.Product.id
    ).filter(
        mod_orders.Order.id == order_id
    ).first()
    
    if not db_order:
        raise HTTPException(status_code= 404, detail= "Pedido não encontrado.")
    
    order_dict = {
        "order_id": db_order.id,
        "user_name": db_order.user_name,
        "products": []
    }
    
    for product in db_order.products:
        product_dict = {
            "product_name": product.name,
            "product_price": product.price,
            "product_quantity": product.quantity
        }
        
        order_dict["products"].append(product_dict)
    
    
    return order_dict