from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from models import mod_users
from schemas import sch_users

router = APIRouter()


@router.post("/users/", response_model= sch_users.User)
def create_user(user: sch_users.User,
                db: Session= Depends(database.get_db)):
    
    db_user = mod_users.User(name= user.name,
                             email= user.email,
                             password=  user.password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/users/{user_id}", response_model= sch_users.User)
def get_user(user_id: int,
             db: Session= Depends(database.get_db)):
    
    db_user = db.query(mod_users.User).filter(mod_users.User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code= 404, detail= "Usuário não encontrado.")
    
    return db_user