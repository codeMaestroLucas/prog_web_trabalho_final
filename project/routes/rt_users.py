from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.mod_users import User as modUser
from ..schemas.sch_users import User as schUser
from ..database import get_db
from ..utils.check_if_exists import check_if_exists
from ..utils.return_formatted_data import return_formatted_data

router = APIRouter(
    tags= ['User Routes'],
    prefix= '/users'
)


@router.post("/create")
def create_user(user: schUser,
                db: Session = Depends(get_db)) -> dict:
    """Função usada para criar um novo usuário.

    Args:
        user (schUser): Usuário que será criado.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Returns:
        dict: O usuário criado.
    """
    try:
        db_user = modUser(name= user.name,
                          email= user.email,
                          password= user.password)
        

        check_if_exists('users', db_user, db, invert= True)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
        return return_formatted_data(db_user, db)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 400, detail= "Email em uso.")
    

@router.get("/{user_id}")
def read_user(user_id: int,
              db: Session = Depends(get_db)) -> dict:
    """Função que retorna um usuário criado baseado no ID.

    Args:
        user_id (int): ID do usuário.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso não haja um ID correspondente ao que foi solicitado.

    Returns:
        dict: Usuário correspondente ao ID solicitado.
    """
    db_query = select(modUser).where(modUser.id == user_id)
    user_to_get = db.execute(db_query).scalars().first()

    check_if_exists('users', user_to_get, db)
    
    return return_formatted_data(user_to_get, db)


@router.put('/{user_id}')
def update_user(user_id: int,
                user: schUser,
                db: Session = Depends(get_db)) -> dict:
    """Função usada para atualizar um usuário basedo no ID.

    Args:
        user_id (int): ID do usuário que será atualizado.
        user (schUser): Novos campos de usuário que serão usados.
        db (Session, optional): Conexão com o DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: Caso o novo email já esteja em uso por outro usuário.

    Returns:
        dict: Usuário atualizado.
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

        return return_formatted_data(user_to_update, db)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 400,
                            detail= "Endereço de email já está em uso.")


@router.delete('/{user_id}')
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