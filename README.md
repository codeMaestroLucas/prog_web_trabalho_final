# Problemas
Dentro de um pedido só cabem UM produto, tem que ser 1 ou vários.

Inserção de dados automaticamente não está funcionando. -> Usar as funções do
backend ao invés de fazer requests.

Integrar as rotas do back com o front. Criar um rota a mais para pegar as
requisições e chamar as funções 

Fazer a parte do MOUNT - Live de 3h

# Ideias
Colocar valores de usuário, produtos e pedidos válidos em um JSON para rodar de
uma vez e trabalhar com as requisições. -> Tentando

Testes;

# Projeto Final

<aside>
📎  Index:

- [Preparando o ambiente](#preparando-o-ambiente)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação](#instalação)
- [Descrição dos Diretórios](#descrição-dos-diretórios)
- [](#)
</aside>

# Preparando o ambiente

Este é um projeto que usa FastAPI, SQLAlchemy, e SQLite para criar uma aplicação web básica.

## Pré-requisitos

- [Docker](https://www.docker.com/)
<!-- - [Docker Compose](https://docs.docker.com/compose/) -->

## Instalação

1. Clone o repositório:
    
    ```powershell
    git clone https://github.com/codeMaestroLucas/prog_web_trabalho_final.git
    ```
    
2. Mude de pasta:
    
    ```powershell
    cd prog_web_trabalho_final
    ```
    
3. Inicie container:
    ```powershell
    docker composer up
    ```

    Isso pode levar alguns segundos.
        
    
4. Acesse a aplicação pelo link http://localhost:8000/ ou http://127.0.0.1:8000/
    
OBS: Para encerrar a aplicação basta, no terminal, pressionar as teclas CTRL + C
ou realizar o comando `docker compose down`

# Descrição dos Diretórios

```powershell
├───project
│   │
│   ├───insert_data
│   │
│   ├───models
│   │
│   ├───routes
│   │
│   ├───schemas
│   │
│   ├───static
│   │
│   ├───templates
```

- **Project:** diretório que contém os arquivos relacionados com todo o Backend
e Frontend da aplicação;
    - **Insert Data:** diretório que contém os dados para serem inseridos
automaticamente no DB.
    - **Models:** diretório que contém as classes estruturadas para o formato de
banco de dados no SQLAlchemy;
    - **Routes:** diretório que contém as rotas (endpoints) que serão usadas no
FastAPI;
    - **Schemas:** diretório que contém os esquemas de dados para validação e
serialização usando Pydantic.
    - **Static:** contém os arquivos estáticos - podendo ser JavaScript, CSS e
imagens - que serão enviados para o cliente;
    - **Templates:** contém os templates em HTML que serão renderizados pelo
FastAPI para criar páginas web.