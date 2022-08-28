import secrets
from statistics import mode
from typing import List
import uuid
from sqlalchemy.orm import Session

from . import models, schemas, auth
from .database import engine, get_db
from .config import *

# User Based CURD functions

def get_user (db: Session, email:str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_aadhaar (db:Session, aadhaar: str) -> models.User : 
    return db.query(models.User).filter(models.User.aadhaar_id == aadhaar).first()
    
def get_bin(db: Session, uid: str) -> models.Bin :
    return db.query(models.Bin).filter(models.Bin.uid == uid).first()

def get_all_bins(db: Session) -> List[models.Bin] : 
    return db.query(models.Bin).all()

def register_user(db: Session, user: schemas.UserNew) :
    new_user = models.User(
        email=user.email,
        name= user.name,
        aadhaar_id=user.aadhaar,
        password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()

# BIN related
def add_bin (db: Session, bin: models.Bin) -> models.Bin : 
    db.add(bin)
    db.commit()
    return db.query(models.Bin).filter(models.Bin.uid == bin.uid).first()

# Transaction related
def add_transaction (db: Session, transaction: schemas.TransactionBase) : 
    waste_type = get_waste_type(db, transaction.waste_type)
    user = get_user(db, email=transaction.email)
    if not user : raise Exception("INvalid user type !")
    if not waste_type : raise Exception("Invalid Waste Type !")
    credits = waste_type.credits * transaction.weight
    user.credit_balance += credits
    new_transaction = models.Transaction(
        uid=uuid.uuid4().hex,
        email=transaction.email,
        bin_uid=transaction.bin_uid,
        waste_type=transaction.waste_type,
        weight=transaction.weight,
        credits=credits
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_all_user_transaction (db:Session, user_email:str) -> List[models.Transaction] : 
    return db.query(models.Transaction).filter(models.Transaction.email == user_email).all()

def get_transaction (db:Session, user_email:str, uid: str) -> models.Transaction | None :
    return db.query(models.Transaction).filter(models.Transaction.email == user_email).filter(models.Transaction.uid == uid).get()

# Waste Type related

def get_all_waste_types (db:Session) -> List[models.WasteType]: 
    return db.query(models.WasteType).all()

def get_waste_type (db:Session, waste_type : str) -> models.WasteType | None: 
    return db.query(models.WasteType).filter(models.WasteType.type == waste_type).first()

