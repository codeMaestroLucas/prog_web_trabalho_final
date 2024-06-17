from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.mod_users import User as modUser
from schemas.sch_users import User as schUser
from database import get_db
from utils import check_if_exists, return_formatted_data

router = APIRouter()

@router.post("/users/", response_model= schUser)
def create_user(user: schUser,
                db: Session = Depends(get_db)) -> modUser:
    """Função usada para criar um novo usuário.

    Args:
        user (schUser): Usuário que será criado.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        modUser: O usuário criado.
    """
    try:
        db_user = modUser(
                                name= user.name,
                                email= user.email,
                                password= user.password
                                )
        

        check_if_exists('users', db_user, db, invert= True)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
        return db_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 400, detail= "Email em uso.")
    

@router.get("/users/{user_id}")
def read_user(user_id: int,
             db: Session = Depends(get_db)) -> dict:
    """Função que retorna um usuário criado baseado no ID.

    Args:
        user_id (int): ID do usuário.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: caso não haja um ID correspondente ao que foi solicitado.

    Returns:
        modUser: Usuário correspondente ao ID solicitado.
    """
    db_query = select(modUser).where(modUser.id == user_id)
    user_to_get = db.execute(db_query).scalars().first()

    check_if_exists('users', user_to_get, db)
    
    return return_formatted_data(user_to_get, db)


@router.put('/users/{user_id}', response_model= schUser)
def update_user(user_id: int,
                user: schUser,
                db: Session = Depends(get_db)) -> modUser:
    """Função usada para atualizar um usuário basedo no ID.

    Args:
        user_id (int): ID do usuário que será atualizado.
        user (schUser): Novos campos de usuário que serão usados.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso o novo email já esteja em uso por outro usuário.

    Returns:
        modUser: Usuário atualizado.
    """
    
    db_query = select(modUser).where(modUser.id == user_id)
    user_to_update = db.execute(db_query).scalars().first()
    
    check_if_exists('user', user_to_update, db)

    stmt = update(modUser).where(modUser.id == user_id).values(
        name= user.name,
        email= user.email,
        password=  user.password
    )

    try:
        db.execute(stmt)
        db.commit()

        updated_user = db.query(modUser).filter(modUser.id == user_id).first()
        return updated_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 400, detail= "Endereço de email já está em uso.")


@router.delete('/user/{user_id}')
def delete_user(user_id: int,
                db: Session = Depends(get_db)) -> dict:
    """Função usada para deletar um usuário baseado no ID.

    Args:
        user_id (int): ID do usuário
        db (Session, optional): Conexão com DB. Defaults to Depends(get_db).

    Returns:
        dict: Mensagem de retorno.
    """
    db_query = select(modUser).where(modUser.id == user_id)
    user_to_delete = db.execute(db_query).scalars().first()
    
    check_if_exists('user', user_to_delete, db)
    
    stmt = delete(modUser).where(modUser.id == user_id)

    db.execute(stmt)
    db.commit()
    
    return {'msg' : 'Usuário deletado.'}