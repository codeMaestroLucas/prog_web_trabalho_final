from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from models import mod_users
from schemas import sch_users

router = APIRouter()


@router.post("/users/", response_model= sch_users.User)
def create_user(user: sch_users.User,
                db: Session= Depends(database.get_db)) -> mod_users.User:
    """Função usada para criar um novo pedido.

    Args:
        user (sch_users.User): Usuário que será criado.
        db (Session, optional): Sessão de banco de dados usada para enviar os
        dados. Defaults to Depends(database.get_db).

    Returns:
        mod_users.User: O usuário criado.
    """
    db_user = mod_users.User(name= user.name,
                             email= user.email,
                             password=  user.password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/users/{user_id}", response_model= sch_users.User)
def get_user(user_id: int,
             db: Session= Depends(database.get_db)) -> mod_users.User:
    """Função usada para retornar usuários que já foram criados.

    Args:
        user_id (int): id do usuário.
        db (Session, optional): Sessão de banco de dados que será usada para
        enviar os dados. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: caso não haja um id correspondente ao que foi solicitado.

    Returns:
        mod_users.User: usuário correspondente ao id solicitado.
    """
    db_user = db.query(mod_users.User).filter(mod_users.User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code= 404, detail= "Usuário não encontrado.")
    
    return db_user