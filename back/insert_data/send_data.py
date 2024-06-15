import json
import requests
import asyncio

async def send_data(file: str, url: str):
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
            await asyncio.sleep(1)
            requests.post(url, json= item)

async def insert_data()-> None:
    """Função usada para inserir dados automaticamente no DB.
    """
    files_and_endpoints: dict = {
        'users.json': 'http://127.0.0.1:8000/users',
        'products.json': 'http://127.0.0.1:8000/products',
        'orders.json': 'http://127.0.0.1:8000/orders'
    }

    BASE_DIR = r'back\\insert_data\\'
    for file, endpoint in files_and_endpoints.items():
        file_path = BASE_DIR + file
        send_data(file_path, endpoint)