from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "database.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///" + DB_PATH


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
Base = declarative_base()

def get_db():
    """Função usada para criar uma conexão e entragá-la para que receba os
    valores necessários. Após as operações serem realizadas a conexão será
    encerrada.

    Yields:
        Session: Conexão com o DB.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()