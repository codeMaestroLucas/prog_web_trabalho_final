from ..schemas.sch_users import User as schUser
from ..models.mod_users import User as modUser
from ..schemas.sch_products import Product as schProduct
from ..models.mod_products import Product as modProduct
from ..schemas.sch_orders import Order as schOrder
from ..models.mod_orders import Order as modOrder
from ..database import get_db
from sqlalchemy.orm import Session
import json

def send_data(file: str, db: Session):
    """Função usada para enviar os dados armazenados em arquivos JSON para o DB
    automaticamente.
    
    As operações com os dados ainda funcionam, essa função serve apenas para
    popular o DB.

    Args:
        file (str): Arquivo JSON que contém os dados.
        db (Session): Sessão do banco de dados.
    """
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        if file.endswith('users.json'):
            for item in data:
                user = modUser(name=item['name'],
                               email=item['email'],
                               password=item['password'])
                db.add(user)
        
        elif file.endswith('products.json'):
            for item in data:
                product = modProduct(name=item['name'],
                                     price=item['price'],
                                     in_stock=item['in_stock'])
                db.add(product)
        
        elif file.endswith('orders.json'):
            for item in data:
                order = modOrder(user_id=item['user_id'],
                                 product_id=item['product_id'],
                                 quantity=item['quantity'])
                db.add(order)
        
        db.commit()

def insert_data()-> None:
    """Função usada para inserir dados automaticamente no DB.
    """

    files: list[str] = ['users.json', 'products.json', 'orders.json']
    
    BASE_DIR = r'project\\insert_data\\'
    for file in files:
        file_path = BASE_DIR + file
        send_data(file_path)
        
def main() -> None:
    """Function used to run the main code."""
    




if __name__ == '__main__':
    main()