from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
<<<<<<< HEAD
import os

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "test.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///" + DB_PATH

=======


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    )

<<<<<<< HEAD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
=======
SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
>>>>>>> 08678f095d92dbbf56a6a0fd5e325b37d0f88342
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()