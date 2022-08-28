from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import *

user, password, port, db = open(DB_CREDENTIALS).read().split(":")

engine = sqlalchemy.create_engine(f"mariadb+mariadbconnector://{user}:{password}@localhost:{port}/{db}", pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db () : 
    db = SessionLocal()
    try : 
        yield db
    finally :
        db.close()

