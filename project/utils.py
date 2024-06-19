from typing import Union, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, update
from fastapi import HTTPException, Depends
from .database import get_db
from .models.mod_orders import Order as modOrder
from .models.mod_products import Product as modProduct
from .models.mod_users import User as modUser
from typing import Union, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from fastapi import HTTPException, Depends
 
 
def _verify_instance(
        to_check: str,
        object_to_check: Union[modOrder, modProduct, modUser, None]
        ) -> Tuple:
    """Função usada para verificar o tipo da instância e retornar os campos para
    serem usados na função 'check_if_exists' ."

    Args:
        to_check (str): String que serve de fallback caso o tipo do objeto seja
        'None'.
        object_to_check (Union[modOrder, modProduct, modUser, None]): Objeto a
        ser verificado.

    Returns:
        Tuple: Retorna os campos 'name_to_check', 'fields_to_check' e
        'table_to_check'.
    """
    if to_check in 'orders' or isinstance(object_to_check, modOrder):
        name_to_check = 'Pedido'
        fields_to_check: Tuple[str] = ('user_id', 'product_id', 'quantity',)
        table_to_check = modOrder
        
    elif to_check in 'users' or isinstance(object_to_check, modUser):
        name_to_check = 'Usuário'
        fields_to_check: Tuple[str] = ('name', 'email')
        table_to_check = modUser

    elif to_check in 'products' or isinstance(object_to_check, modProduct):
        name_to_check = 'Produto'
        fields_to_check: Tuple[str] = ('name', 'price', 'in_stock')
        table_to_check = modProduct
    
    return name_to_check, fields_to_check, table_to_check


def check_if_exists(
    to_check: str,
    object_to_check: Union[modOrder, modProduct, modUser, None],
    db: Session = Depends(get_db),
    invert: bool = False) -> None:
    """Função usada para verificar a existência ou não de um Pedido, Produto ou
    Usuário.

    Args:
        to_check (str): Tabela que será verificada. Normalmente esse campo é
        utilizado para garantir uma redundância, caso o Objeto fornecido seja do
        tipo None.
        object_to_check (Union[modOrder, modProduct, modUser, None]): Objeto a
        ser verificado.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).
        invert (bool, optional): Altera o funcionamento da função.
        Defaults to False.
        
        - ivert= False: A função buscará por um objeto que já existe no DB. Util
        na hora de se pegar um objeto, fazer o update e deletá-lo.
        - ivert= True: A função buscará por um objeto que não existe no DB. Util
        na hora de se criar um objeto.

    Raises:
        HTTPException: Caso o objeto não exista no DB.
    """
    name_to_check, fields_to_check, table_to_check = _verify_instance(to_check,object_to_check)

    conditions: List[str] = []
    try:
        for field in fields_to_check:
            field_value = getattr(object_to_check, field)
            conditions.append(getattr(table_to_check, field) == field_value)

        query = select(table_to_check).where(and_(*conditions))
        exists = db.execute(query).scalars().first()
        
        if invert:
            if exists:
                db.rollback()
                raise HTTPException(status_code= 400,
                                    detail= f"{name_to_check} já existe.")
        else:
            if not exists:
                db.rollback()
                raise HTTPException(status_code= 400,
                                    detail= f"{name_to_check} não existe.")
            
    except AttributeError:
        db.rollback()
        raise HTTPException(status_code= 400,
                                detail= f"{name_to_check} não existe.")


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


def verify_quantity(order: modOrder,
                    quantity: int, db: Session = Depends(get_db)) -> int:
    """Função usada para verificar a quantidade em estoque e atualizá-la
    conforme o necessário.

    Args:
        order (modOrder): Pedido.
        quantity (int): Quantidade.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso o produto não tenha sido encontrado.
        HTTPException: Caso não haja nenhum produto em estoque.
        HTTPException: Caso a quantidade seja maior do que o valor em estoque.

    Returns:
        int: Quantidade.
    """
    stmt = select(modProduct.in_stock).where(modProduct.id == order.product_id)
    result = db.execute(stmt).first()

    if not result:
        db.rollback()
        raise HTTPException(status_code= 404, detail= "Produto não encontrado.")

    in_stock = result[0]

    if in_stock == 0:
        if quantity > 0: # Para quando a quantidade for "zero" e o produto for deletado.
            db.rollback()
            raise HTTPException(status_code= 404, detail= "Adicione mais produtos no \
estoque para poder continuar.")

    if in_stock - quantity < 0:
        db.rollback()
        raise HTTPException(status_code= 404, detail= f"Quantidade indisponível \
para retirada. Temos apenas {in_stock} desse produto em estoque.")
    
    
    update_stmt = (
        update(modProduct)
        .where(modProduct.id == order.product_id)
        .values(in_stock= in_stock - quantity)
    )
    db.execute(update_stmt)
    db.commit()
    
    return quantity

def check_len_table(): ...
def insert_data(): ...