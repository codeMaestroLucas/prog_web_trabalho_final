from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.mod_orders import Order as modOrder
from models.mod_products import Product as modProduct
from models.mod_users import User as modUser
from schemas.sch_orders import Order as schOrder
from database import get_db
from utils import check_if_exists, return_order_formated

router = APIRouter()


def check_if_order_exists(order: modOrder,
                    db: Session = Depends(get_db),
                    invert: bool = False) -> None:
    """Função usada para verificar se um pedido existe ou não no DB.

    Args:
        order (modOrder): Pedido que será verificado a sua existência ou
        não no DB.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).
        invert (Bool): Modifica o funcionamento da função, sendo usado para
        saber se a resposta deve ser positiva ou negativa da consulta. O padrão
        é 'False' que verifica se o pedido JÁ EXISTE. Já quando está para
        'TRUE' verifica se o pedido NÃO EXISTE.

    Raises:
        HTTPException: Caso o pedido já exista.
        
    Exception:
        Except (AttributeError): Esse except acontece quando o resultado da
        query é NoneType.
    """
    try:
        exists_order = db.query(modOrder).filter(
            modOrder.user_id == order.user_id,
            modOrder.product_id == order.product_id,
            modOrder.quantity == order.quantity
        ).first()


        if invert:
            if exists_order:
                raise HTTPException(status_code= 400,
                                    detail= "Pedido já existe.")
        
        else:
            if not exists_order:
                raise HTTPException(status_code= 400,
                                    detail= "Pedido não existe.")

    except AttributeError:
        raise HTTPException(status_code= 400,
                            detail= "Pedido não existe.")
    
    
def check_if_user_exists(order: modOrder,
                         db: Session = Depends(get_db)) -> None:
    """Função usada para verificar se o usuário existe ou não na tabela de
    usuários.

    Args:
        order (modOrder): Novo pedido.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso o usuário não exista.
    """
    stmt = select(modUser).where(modUser.id == order.user_id)
    db_user = db.execute(stmt).first()

    if not db_user:
        raise HTTPException(status_code= 400,
                            detail= "Usuário não existe.")


def check_if_product_exists(order: modOrder,
                            db: Session = Depends(get_db)) -> None:
    """Função usada para verificar se o produto existe ou não na tabela de
    produtos.

    Args:
        order (modOrder): Novo pedido.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso o produto não exista.
    """
    stmt = select(modProduct).where(modProduct.id == order.product_id)
    db_product = db.execute(stmt).first()
    
    if not db_product:
        raise HTTPException(status_code= 400,
                            detail= "Produto não existe.")


def check_if_exists(old_order: modOrder,
                    new_order: modOrder,
                    db: Session = Depends(get_db)):
    """Função usada para verficar a existencia do pedido, levando em conta a
    existência dos usuários e produtos nas suas respectivas tabelas.
    
    Essa função ficará responsável por chamar todas as verificações individuais.

    Args:
        old_order (modOrder): Pedido que receberá a alteração.
        new_order (modOrder): Novos campos de pedido.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).
    
    Raises:
        HTTPException: Caso os o pedido com os campos alterados coincidam com
        outro já registrado na tabela ORDERS.
    """
    check_if_order_exists(old_order, db)
    check_if_user_exists(new_order, db)
    check_if_product_exists(new_order, db)
    
    stmt = select(modOrder).where(
        modOrder.user_id == new_order.user_id,
        modOrder.product_id == new_order.product_id)
    db_order = db.execute(stmt).scalars().first()
    
    if db_order:
        raise HTTPException(status_code= 400,
                            detail= "Pedido já existe.")





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
        int: A quantidade.
    """
    stmt = select(modProduct.in_stock).where(modProduct.id == order.product_id)
    result = db.execute(stmt).first()

    if not result:
        raise HTTPException(status_code= 404, detail= "Produto não encontrado.")

    in_stock = result[0]

    if in_stock == 0:
        raise HTTPException(status_code= 404, detail= "Adicione mais produtos no \
estoque para poder continuar.")

    if in_stock - quantity < 0:
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


def calculate_total_value(order: schOrder,
                          db: Session = Depends(get_db)) -> float:
    """Função usada para calcular o valor total do pedido.

    Args:
        order (modOrder): Pedido.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso o pedido não seja enconrtado.

    Returns:
        float: Valor total do pedido.
    """
    stmt = select(modProduct.price).where(modProduct.id == order.product_id)
    db_order = db.execute(stmt).first()

    if db_order:
        price = db_order[0]
        price, order.quantity
        return round(price * order.quantity, 2)

    else:
        db.rollback()
        raise HTTPException(status_code= 404, detail= "Pedido não encontrado ou inválido.")


@router.post("/orders/", response_model= schOrder)
def create_order(order: schOrder,
                db: Session = Depends(get_db)) -> modOrder:
    """Função usada para criar um novo pedido.

    Args:
        order (schOrder): Pedido que será criado.
        db (Session, optional): Sessão de banco de dados usada para enviar os
        dados. Defaults to Depends(get_db).

    Returns:
        modOrder: O pedido criado.
    """
    db_order = modOrder(
                        user_id= order.user_id,
                        product_id= order.product_id,
                        quantity= verify_quantity(order, order.quantity, db),
                        total_value= calculate_total_value(order, db)
                        )
    
    check_if_order_exists(db_order, db, invert= True)
    check_if_user_exists(db_order, db)
    check_if_product_exists(db_order, db)

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


@router.get("/orders/{order_id}")
def read_order(order_id: int,
             db: Session = Depends(get_db)):
    """Função que retorna um pedido criado baseado no ID.

    Args:
        order_id (int): ID do pedido.
        db (Session, optional): Sessão de banco de dados que será usada para
        enviar os dados. Defaults to Depends(get_db).

    Raises:
        HTTPException: caso não haja um ID correspondente ao que foi solicitado.

    Returns:
        modOrder: pedido correspondente ao ID solicitado.
    """
    db_query = select(modOrder).where(modOrder.id == order_id)
    order_to_get = db.execute(db_query).scalars().first()

    check_if_order_exists(order_to_get, db)
    
    return return_order_formated(order_to_get, db)


@router.put('/orders/{order_id}', response_model= schOrder)
def update_order(order_id: int,
                order: schOrder,
                db: Session = Depends(get_db)) -> modOrder:
    """Função usada para atualizar um pedido basedo no ID.

    Args:
        order_id (int): ID do pedido que será atualizado.
        order (schOrder): Novos campos de pedido que serão usados.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        modOrder: Pedido atualizado.
    """
    db_query = select(modOrder).where(modOrder.id == order_id)
    old_order = db.execute(db_query).scalars().first()
    
    check_if_exists(old_order, order, db)
    
    to_remove = order.quantity - old_order.quantity
    verify_quantity(old_order, to_remove, db)
    
    stmt = update(modOrder).where(modOrder.id == order_id).values(
        user_id= order.user_id,
        product_id= order.product_id,
        quantity= order.quantity,
        total_value= calculate_total_value(order, db)
    )

    try:
        db.execute(stmt)
        db.commit()

        updated_order = db.query(modOrder).filter(modOrder.id == order_id).first()
        return updated_order

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 400, detail= "Erro ao atualizar o pedido.")


@router.delete('/order/{order_id}')
def delete_order(order_id: int,
                db: Session = Depends(get_db)) -> str:
    """Função usada para deletar um pedido baseado no ID.

    Args:
        order_id (int): ID do pedido.
        db (Session, optional): Conexão com DB. Defaults to Depends(get_db).

    Returns:
        str: Mensagem de retorno.
    """
    db_query = select(modOrder).where(modOrder.id == order_id)
    order_to_delete = db.execute(db_query).scalars().first()
    
    check_if_order_exists(order_to_delete, db)
    
    stmt = delete(modOrder).where(modOrder.id == order_id)

    try:
        db.execute(stmt)
        db.commit()
        
        return 'Pedido deletado.'
    
    except:
        db.rollback()
        return 'Falha ao deletar o pedido.'