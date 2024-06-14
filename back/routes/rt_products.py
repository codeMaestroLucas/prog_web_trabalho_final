from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from models.mod_products import Product as modProduct
from schemas.sch_products import Product as schProduct
from database import get_db

router = APIRouter()

def check_if_exists(product: modProduct,
                    db: Session = Depends(get_db),
                    invert: bool = False) -> None:
    """Função usada para verificar se um produto existe ou não no DB.
    
    Args:
        product (modProduct): Produto que será verificado a sua existência ou
        não no DB.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).
        invert (Bool): Modifica o funcionamento da função, sendo usado para
        saber se a resposta deve ser positiva ou negativa da consulta. O padrão
        é 'False' que verifica se o produto JÁ EXISTE. Já quando está para
        'TRUE' verifica se o produto NÃO EXISTE.

    Raises:
        HTTPException: Caso o produto já exista.
        
    Exception:
        Except (AttributeError): Esse except acontece quando o resultado da
        query é NoneType.
    """
    try:
        exists = db.query(modProduct).filter(modProduct.name == product.name).first()

        if invert:
            if exists:
                raise HTTPException(status_code= 400,
                                    detail= "Produto já existe.")
        
        else:
            if not exists:
                raise HTTPException(status_code= 400,
                                    detail= "Produto não existe.")

    except AttributeError:
        raise HTTPException(status_code= 400,
                            detail= "Produto não existe.")
        

@router.post("/products/", response_model= schProduct)
def create_product(product: schProduct,
                db: Session = Depends(get_db)) -> modProduct:
    """Função usada para criar um novo produto.

    Args:
        product (schProduct): Produto que será criado.
        db (Session, optional): Sessão de banco de dados usada para enviar os
        dados. Defaults to Depends(get_db).

    Returns:
        modProduct: O produto criado.
    """
    db_product = modProduct(
                            name= product.name,
                            price= product.price,
                            quantity=  product.quantity
                            )
    
    check_if_exists(db_product, db, invert= True)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@router.get("/products/{product_id}", response_model= schProduct)
def read_product(product_id: int,
             db: Session = Depends(get_db)) -> modProduct:
    """Função que retorna um produto criado baseado no ID.

    Args:
        product_id (int): ID do produto.
        db (Session, optional): Sessão de banco de dados que será usada para
        enviar os dados. Defaults to Depends(get_db).

    Raises:
        HTTPException: caso não haja um ID correspondente ao que foi solicitado.

    Returns:
        modProduct: produto correspondente ao ID solicitado.
    """
    db_query = select(modProduct).where(modProduct.id == product_id)
    product_to_get = db.execute(db_query).scalars().first()

    check_if_exists(product_to_get, db)
    
    return product_to_get


@router.put('/products/{product_id}', response_model= schProduct)
def update_product(product_id: int,
                product: schProduct,
                db: Session = Depends(get_db)) -> modProduct:
    """Função usada para atualizar um produto basedo no ID.

    Args:
        product_id (int): ID do produto que será atualizado.
        product (schProduct): Novos campos de produto que serão usados.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso o novo email já esteja em uso por outro produto.

    Returns:
        modProduct: Produto atualizado.
    """
    
    db_query = select(modProduct).where(modProduct.id == product_id)
    product_to_update = db.execute(db_query).scalars().first()
    
    check_if_exists(product_to_update, db)
    
    stmt = update(modProduct).where(modProduct.id == product_id).values(
        name= product.name,
        price= product.price,
        quantity=  product.quantity
    )

    db.execute(stmt)
    db.commit()

    updated_product = db.query(modProduct).filter(modProduct.id == product_id).first()
    return updated_product


@router.delete('/product/{product_id}', response_model= None)
def delete_product(product_id: int,
                db: Session = Depends(get_db)) -> str:
    """Função usada para deletar um produto baseado no ID.

    Args:
        product_id (int): ID do produto
        db (Session, optional): Conexão com DB. Defaults to Depends(get_db).

    Returns:
        str: Mensagem de retorno.
    """
    db_query = select(modProduct).where(modProduct.id == product_id)
    product_to_delete = db.execute(db_query).scalars().first()
    
    check_if_exists(product_to_delete, db)
    
    stmt = delete(modProduct).where(modProduct.id == product_id)

    try:
        db.execute(stmt)
        db.commit()
        
        return {'msg' : 'Produto deletado.'}
    
    except:
        db.rollback()
        return {'msg' : 'Falha ao deletar o produto.'}