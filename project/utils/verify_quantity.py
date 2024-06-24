from sqlalchemy.orm import Session
from sqlalchemy import select, update
from fastapi import HTTPException, Depends
from ..database import get_db
from ..models.mod_orders import Order as modOrder
from ..models.mod_products import Product as modProduct
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, Depends
 

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
            raise HTTPException(status_code= 404, detail= "Adicione mais \
produtos no estoque para poder continuar.")

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