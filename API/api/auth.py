import hashlib
import itertools
from datetime import datetime, timedelta
from typing import List, Tuple
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext


from . import schemas,models
from .config import *

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/moneyplant/auth/token",
    scopes={
        USER_TYPE : "to access user information paths",
        BIN_TYPE : "to access bin information path"
    })
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token (data : schemas.User | schemas.BinBase, type: str) -> str:
    if type == USER_TYPE : user = data.email
    elif type == BIN_TYPE : user = data.uid
    to_encode = {
        "scopes": [type],
        "user" : user,
        "exp" : datetime.utcnow() + timedelta(minutes=TOKEN_VALIDITY_TIME)
        }
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM )


def verify_password (password : str, given_password: str) :
    try :
        return pwd_context.verify(given_password, password)
    except :
        return False

def hash_password (password : str) -> str :
    return pwd_context.hash(password)

def get_data_from_token (token: str = Depends(oauth2_scheme)) -> Tuple[str, Tuple[str]] | None: 
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("user")
        scopes : Tuple[str] = payload.get("scopes")
        if  email : return email, scopes
    except JWTError:
        return None

