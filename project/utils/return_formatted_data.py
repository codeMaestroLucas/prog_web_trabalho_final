from typing import Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from ..database import get_db
from ..models.mod_orders import Order as modOrder
from ..models.mod_products import Product as modProduct
from ..models.mod_users import User as modUser
from sqlalchemy.orm import Session
 

def _return_formatted_user(obj: modUser,
                          db: Session = Depends(get_db)) -> dict:
    """Função usada para formatar a saída do usuário quando solicitado.

    Args:
        obj (modUser): Usuário.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        dict: Usuário formatado.
    """
    stmt = select(modUser.id, modUser.name, modUser.email).where(modUser.id == obj.id)
    result = db.execute(stmt).first()

    formatted_data = {
        'id': result[0],
        'name': result[1],
        'email': result[2]
    }
    
    return formatted_data

    
def _return_formatted_product(obj: modProduct,
                          db: Session = Depends(get_db)) -> dict:
        """Função usada para formatar a saída do produto quando solicitado.

    Args:
        obj (modUser): Produto.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        dict: Produto formatado.
    """
        stmt = select(modProduct.id,
                      modProduct.name,
                      modProduct.price,
                      modProduct.in_stock)\
            .where(modProduct.id == obj.id)
        result = db.execute(stmt).first()
        
        formatted_data = {
            'id': result[0],
            'name': result[1],
            'price': f'${result[2]:.2f}',
            'in_stock': result[3]
        }
        
        return formatted_data
    
    
def _return_formatted_order(obj: modOrder,
                          db: Session = Depends(get_db)) -> dict:
    """Função usada para formatar a saída do pedido quando solicitado.

    Args:
        obj (modUser): Pedido.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        dict: Pedido formatado.
    """
    stmt = select(modOrder.id,
                modUser.name,
                modProduct.name, modProduct.price,
                modOrder.quantity).\
        join(modUser).join(modProduct).\
        where(modOrder.id == obj.id)
    
    result = db.execute(stmt).first()

    formatted_data = {
        'id': result[0],
        'user_name': result[1],
        'product_name': result[2],
        'product_unitary_price': f'${result[3]:.2f}',
        'product_quantity': f'{result[4]}x',
        'total_value': f'${(result[3] * result[4]):.2f}'
    }
    
    return formatted_data
    
    
def return_formatted_data(
    obj: Union[modOrder, modProduct, modUser],
    db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Função usada para formatar a saída de um objeto 'modOrder', 'modProduct'
    ou 'modUser'.

    Args:
        obj (Union[modOrder, modProduct, modUser]): Objeto a ser formatado.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        dict: Dicionário com os dados formatados.
    """
    if isinstance(obj, modUser):
        formatted_data = _return_formatted_user(obj, db)

    elif isinstance(obj, modProduct):
        formatted_data = _return_formatted_product(obj, db)
        
    elif isinstance(obj, modOrder):
        formatted_data = _return_formatted_order(obj, db)
        
    else:
        raise ValueError("Tipo de objeto não suportado para formatação.")
    
    return formatted_data


def _html_format_product(data: tuple) -> dict:
    """Função usada para formatar o produto de forma que ele possa ser
    apresentado na 'HOME.html'.

    Args:
        data (tuple): Dados do produto.

    Returns:
        dict: Produto formatado.
    """
    return {
        'id': data[0],
        'name': data[1],
        'price': f'${data[2]:.2f}',
        'in_stock': data[3]
    }

def _html_format_order(data: tuple) -> dict:
    """Função usada para formatar o pedido de forma que ele possa ser
    apresentado na 'HOME.html'.

    Args:
        data (tuple): Dados do pedido.

    Returns:
        dict: Pedido formatado.
    """
    return {
        'id': data[0],
        'user_name': data[1],
        'product_name': data[2],
        'product_unitary_price': f'${data[3]:.2f}',
        'product_quantity': f'{data[4]}x',
        'total_value': f'${(data[3] * data[4]):.2f}'
    }

def html_formatted(db: Session = Depends(get_db)) -> tuple:
    """Função usada para retornar os produtos e pedidos formatados de modo que
    possam ser usados na 'HOME.html'.

    Args:
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        tuple: Dados formatados em Lista.
    """
    stmt_products = select(modProduct.id,
                           modProduct.name,
                           modProduct.price,
                           modProduct.in_stock)
    products = db.execute(stmt_products).all()
    formatted_products = [_html_format_product(prod) for prod in products]

    stmt_orders = select(
        modOrder.id,
        modUser.name,
        modProduct.name,
        modProduct.price,
        modOrder.quantity
                        ).join(modUser).join(modProduct)
    orders = db.execute(stmt_orders).all()
    formatted_orders = [_html_format_order(order) for order in orders]
    
    return formatted_products, formatted_orders