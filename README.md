# Problemas
Dentro de um pedido só cabem UM produto, tem que ser 1 ou vários.

Inserção de dados automaticamente não está funcionando.

Ajeitar rotas dps da criação do Utils.py.

    - Testar dnv os endpoints.

# Ideias
Colocar valores de usuário, produtos e pedidos válidos em um JSON para rodar de uma vez e trabalhar com as requisições. -> Tentando

Docker -> DUVIDA

Testes;

# Projeto Final

<aside>
📎  Index:

- [Preparando o ambiente](#preparando-o-ambiente)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação](#instalação)
- [Descrição dos Diretórios](#descrição-dos-diretórios)
- [](#)
- [](#)
- [](#)
    

</aside>

# Preparando o ambiente

Este é um projeto que usa FastAPI, SQLAlchemy, e SQLite para criar uma aplicação web básica.

## Pré-requisitos

- Python 3.7 ou superior;
- `pip` (gerenciador de pacotes do Python).

## Instalação

1. Clone o repositório:
    
    ```powershell
    git clone https://github.com/codeMaestroLucas/prog_web_trabalho_final.git
    ```
    
2. Crie um ambiente virtual:
    
    ```powershell
    python -m venv venv
    ```
    
3. Inicie o ambiente virtual:
    1. Windows:
        
        ```powershell
        venv\Scripts\activate
        ```
        
    2. MAC ou Linux:
        
        ```powershell
        git add .venv/bin/activate
        ```
        
    
4. Instale as dependências necessárias listas no arquivo “requirements.txt”:
    
    ```powershell
    pip install -r requirements.txt
    ```
    
    Isso pode levar alguns segundos.
    

# Descrição dos Diretórios

```powershell
├───back
│   ├───insert_data
│   │
│   ├───models
│   │
│   ├───routes
│   │
│   ├───schemas
│   │
│   │
└───front
    ├───static
    │
    └───templates
```

- **Back:** diretório que contém os arquivos relacionados com o Backend;
    - **Insert Data:** diretório que contém os dados para serem inseridos automaticamente no DB.
    - **Models:** diretório que contém as classes estruturadas para o formato de banco de dados no SQLAlchemy;
    - **Routes:** diretório que contém as rotas (endpoints) que serão usadas no FastAPI;
    - **Schemas:** diretório que contém os esquemas de dados para validação e serialização usando Pydantic.
- **Front:** diretório que contém os arquivos relacionados com o Frontend.
    - **Static:** contém os arquivos estáticos - JavaScript, CSS e imagens - que serão enviados para o cliente;
    - **Templates:** contém os templates em HTML que serão renderizados pelo FastAPI para criar páginas web.