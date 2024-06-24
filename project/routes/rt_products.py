from fastapi import Depends, Request, Form, APIRouter
from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from ..models.mod_products import Product as modProduct
from ..schemas.sch_products import Product as schProduct
from ..database import get_db
from ..utils.check_if_exists import check_if_exists
from ..utils.return_formatted_data import return_formatted_data

router = APIRouter(
    tags= ['Product Routes']
)

# def request_create_product(request: Request,
#                            db: Session = Depends(get_db),
#                            name: str = Form(...),
#                            price: float = Form(...),
#                            in_stock:int = Form(...)) -> schProduct:
#     """Função usada para recebero request ao criar um produto e transformá-lo em
#     um schema para fazer a validação."

#     Args:
#         request (Request): Request do HTML.
#         db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).
#         name (str, optional): Nome. Defaults to Form(...).
#         price (float, optional): Preço. Defaults to Form(...).
#         in_stock (int, optional): Quantidade de produtos em estoque. Defaults to
#         Form(...).

#     Returns:
#         schProduct: _description_
#     """
#     product = schProduct(
#         name= name,
#         price= price,
#         in_stock= in_stock
#     )
#     return product



@router.post("/products/create", response_model= schProduct)
def create_product(product: schProduct,
                   db: Session = Depends(get_db)) -> modProduct:
    """Função usada para criar um novo produto.

    Args:
        product (schProduct): Produto que será criado.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        modProduct: O produto criado.
    """
    db_product = modProduct(
                            name= product.name,
                            price= product.price,
                            in_stock=  product.in_stock
                            )
    
    check_if_exists('products', db_product, db, invert= True)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@router.get("/products/read/{product_id}")
def read_product(product_id: int,
             db: Session = Depends(get_db)):
    """Função que retorna um produto criado baseado no ID.

    Args:
        product_id (int): ID do produto.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso não haja um ID correspondente ao que foi solicitado.

    Returns:
        modProduct: Produto correspondente ao ID solicitado.
    """
    db_query = select(modProduct).where(modProduct.id == product_id)
    product_to_get = db.execute(db_query).scalars().first()

    check_if_exists('products', product_to_get, db)
    
    return return_formatted_data(product_to_get, db)


@router.put('/products/update/{product_id}', response_model= schProduct)
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
    
    check_if_exists('products', product_to_update, db) # Old
    
    new_product = modProduct(
                    name= product.name,
                    price= product.price,
                    in_stock=  product.in_stock
                    )
    
    check_if_exists('products', new_product, db, invert= True)
    
    stmt = update(modProduct).where(modProduct.id == product_id).values(
        name= product.name,
        price= product.price,
        in_stock=  product.in_stock
    )
    db.execute(stmt)
    db.commit()

    return new_product


@router.delete('/product/delete/{product_id}')
def delete_product(product_id: int,
                db: Session = Depends(get_db)) -> dict:
    """Função usada para deletar um produto baseado no ID.

    Args:
        product_id (int): ID do produto
        db (Session, optional): Conexão com DB. Defaults to Depends(get_db).

    Returns:
        dict: Mensagem de retorno.
    """
    db_query = select(modProduct).where(modProduct.id == product_id)
    product_to_delete = db.execute(db_query).scalars().first()
    
    check_if_exists('products', product_to_delete, db)
    
    stmt = delete(modProduct).where(modProduct.id == product_id)

    db.execute(stmt)
    db.commit()
    
    return {'msg' : 'Produto deletado.'}