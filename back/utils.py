from typing import Union, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from fastapi import HTTPException, Depends
from database import get_db
from models.mod_orders import Order as modOrder
from models.mod_products import Product as modProduct
from models.mod_users import User as modUser

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
        
        - ivert= False: a função buscará por um objeto que já existe no DB. Util
        na hora de se pegar um objeto, fazer o update e deletá-lo.
        - ivert= True: a função buscará por um objeto que não existe no DB. Util
        na hora de se criar um objeto e fazer o update.

    Raises:
        HTTPException: Caso o objeto não exista no DB.
    """

    print('TO_CHECK: ', to_check)
    print('OBJ: ', object_to_check)
    print('DB: ', db)
    print('INVERT: ', invert)
    print('='*100)

    if to_check in 'orders' or isinstance(object_to_check, modOrder):
        name_to_check = 'Pedido'
        fields_to_check: Tuple[str] = ('user_id', 'product_id', 'quantity',)
        table_to_check = modOrder
        
    elif to_check in 'users' or isinstance(object_to_check, modUser):
        name_to_check = 'Usuário'
        fields_to_check: Tuple[str] = ('name',)
        table_to_check = modUser

    elif to_check in 'products' or isinstance(object_to_check, modProduct):
        name_to_check = 'Produto'
        fields_to_check: Tuple[str] = ('name',)
        table_to_check = modProduct
        
    else:
        raise HTTPException(status_code= 400,
                            detail= f"{name_to_check} não existe.")

    print('Nome do objeto a verificar:', name_to_check)
    print('Campos a verificar:', fields_to_check)
    print('Tabela a verificar:', table_to_check)
    print('='*100)

    conditions: List[str] = []
    
    try:
        for field in fields_to_check:
            field_value = getattr(object_to_check, field)
            conditions.append(getattr(table_to_check, field) == field_value)

        query = select(table_to_check).where(and_(*conditions))
        print('CONDITIONS:', conditions)
        print('Query SQL gerada:', query)

        exists = db.execute(query).scalars().first()
        print('Exists:', exists)

        if invert:
            if exists:
                raise HTTPException(status_code= 400,
                                    detail= f"{name_to_check} já existe.")
        else:
            if not exists:
                raise HTTPException(status_code= 400,
                                    detail= f"{name_to_check} não existe.")
            
    except AttributeError:
            raise HTTPException(status_code= 400,
                                detail= f"{name_to_check} não existe.")

    finally:
        print('#'*100)

        

def return_order_formated(order: modOrder,
                          db: Session = Depends(get_db)) -> dict:
    """Função usada para formatar a saída da função 'GET_ORDER' mostrando os
    campos de 'id_order, 'user_name, 'product_name, 'product_price' e
    'product_quantity'.

    Args:
        order (modOrder): Pedido.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        dict: Dicionário que contém os campos selecionados.
    """
    stmt = select(modOrder.id,
                  modUser.name,
                  modProduct.name, modProduct.price,
                  modOrder.quantity, modOrder.total_value).\
            join(modUser).join(modProduct).\
            where(modOrder.id == order.id)
    
    _order = db.execute(stmt).first()

    order_data: dict = {}
    order_data['id'] = _order[0]
    order_data['user_name'] = _order[1]
    order_data['product_name'] = _order[2]
    order_data['product_unitary_price'] = f'${_order[3]:.2f}'
    order_data['product_quantity'] = f'{_order[4]}x'
    order_data['total_value'] = f'${_order[5]:.2f}'

    return order_data