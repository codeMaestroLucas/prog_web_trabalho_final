from typing import Union, Tuple, List
from ..database import get_db
from ..models.mod_orders import Order as modOrder
from ..models.mod_products import Product as modProduct
from ..models.mod_users import User as modUser
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import select, and_
from fastapi.exceptions import HTTPException


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