from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from dataclasses import dataclass
from ..models.mod_orders import Order as modOrder
from ..models.mod_products import Product as modProduct
from ..models.mod_users import User as modUser
from ..schemas.sch_orders import Order as schOrder
from ..database import get_db
from ..utils.check_if_exists import check_if_exists
from ..utils.return_formatted_data import return_formatted_data
from ..utils.verify_quantity import verify_quantity

router = APIRouter(
    tags= ['Order Routes'],
    prefix= '/orders'
)


@dataclass
class order_input():
    user_id: int  = Form(...)
    product_id: int = Form(...)
    quantity: int = Form(...)

def check_if_order_exists(db_order: modOrder,
                          db: Session = Depends(get_db),
                          invert= False):
    """Função usada para chamar todas as verificações necessárias para os pedidos.

    Args:
        db_order (modOrder): Pedido a ser verificado
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).
        invert (bool, optional): Altera o funcionamento da função. Defaults to False.
    """
    if invert:
        check_if_exists('order', db_order, db, invert= True)
    else:
        check_if_exists('order', db_order, db)

    stmt = select(modUser).where(modUser.id == db_order.user_id)
    db_user = db.execute(stmt).scalars().first()
    check_if_exists('user', db_user, db)

    stmt = select(modProduct).where(modProduct.id == db_order.product_id)
    db_product = db.execute(stmt).scalars().first()
    check_if_exists('product', db_product, db)


@router.post("/create")
def create_order(order: order_input = Depends(),
                 db: Session = Depends(get_db)) -> RedirectResponse:
    """Função usada para criar um novo pedido.

    Args:
        order (order_input): Pedido que será criado.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: para a página home já atualizada.
    """
    order = schOrder(user_id= order.user_id,
                     product_id= order.product_id,
                     quantity= order.quantity,
    )
    
    db_order = modOrder(user_id= order.user_id,
                        product_id= order.product_id,
                        quantity= verify_quantity(order, order.quantity, db),
                        )
    check_if_order_exists(db_order, db, invert= True)
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return RedirectResponse("/home", status_code=303)


@router.get("/{order_id}")
def read_order(order_id: int,
               db: Session = Depends(get_db)) -> dict:
    """Função que retorna um pedido criado baseado no ID.

    Args:
        order_id (int): ID do pedido.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso não haja um ID correspondente ao que foi solicitado.

    Returns:
        dict: Pedido correspondente ao ID solicitado.
    """
    db_query = select(modOrder).where(modOrder.id == order_id)
    order_to_get = db.execute(db_query).scalars().first()

    check_if_order_exists(order_to_get, db)
    
    return return_formatted_data(order_to_get, db)


@router.put('update/{order_id}')
def update_order(order_id: int,
                order: order_input,
                db: Session = Depends(get_db)) -> RedirectResponse:
    """Função usada para atualizar um pedido basedo no ID.

    Args:
        order_id (int): ID do pedido que será atualizado.
        order (order_input): Novos campos de pedido que serão usados.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: para a página home já atualizada.
    """
    db_query = select(modOrder).where(modOrder.id == order_id)
    order_to_update = db.execute(db_query).scalars().first()
    
    check_if_order_exists('order', order_to_update, db)
    
    quantity_to_remove = order.quantity - order_to_update.quantity
    verify_quantity(order_to_update, quantity_to_remove, db)
    
    
    stmt = update(modOrder).where(modOrder.id == order_id).values(
        user_id= order.user_id,
        product_id= order.product_id,
        quantity= order.quantity
    )

    new_order = modOrder(user_id= order.user_id,
                         product_id= order.product_id,
                         quantity= verify_quantity(order, order.quantity, db),
                    )
    check_if_order_exists(new_order, db, invert= True)

    db.execute(stmt)
    db.commit()

    return RedirectResponse(url='/home', status_code= 303)


@router.delete('/{order_id}')
def delete_order(order_id: int,
                db: Session = Depends(get_db)) -> dict:
    """Função usada para deletar um pedido baseado no ID.

    Args:
        order_id (int): ID do pedido.
        db (Session, optional): Conexão com DB. Defaults to Depends(get_db).

    Returns:
        dict: Mensagem de retorno.
    """
    db_query = select(modOrder).where(modOrder.id == order_id)
    order_to_delete = db.execute(db_query).scalars().first()
    
    check_if_order_exists(order_to_delete, db)

    quantity_to_add = order_to_delete.quantity * (-1)
    verify_quantity(order_to_delete, quantity_to_add, db)
    
    
    stmt = delete(modOrder).where(modOrder.id == order_id)

    db.execute(stmt)
    db.commit()
    
    return {'msg' : 'Pedido deletado.'}