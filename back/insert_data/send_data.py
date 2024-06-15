import json
import requests

def send_data(file: str, url: str):
    """Função usada para enviar os dados armazenados em arquivos JSON para o DB
    automaticamente.
    
    As operações com os dados ainda funcionam, essa função serve apenas para
    popular o DB.

    Args:
        file (str): arquivo JSON que contém os dados.
        url (str): url do endpoint que os dados serão enviados.
    """
    with open(file, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
    for item in data:
        requests.post(url, json= item)


def insert_data()-> None:
    """Função usada para inserir dados automaticamente no DB.
    """
    files_and_endpoints: dict = {
        'users.json': 'http://localhost:8000/users',
        'products.json': 'http://localhost:8000/products',
        'orders.json': 'http://localhost:8000/orders'
    }

    for file, endpoint in files_and_endpoints.items():
        send_data(file, endpoint)