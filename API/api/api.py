from multiprocessing import AuthenticationError
import secrets
import uuid
from urllib import response
from api.config import BASE, BASE_URL, BIN_TYPE, USER_TYPE

from fastapi import FastAPI, Depends, HTTPException, status, Form, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from sqlalchemy.orm import Session
import re

from . import schemas, curd, auth, models
from .database import engine, get_db

models.Base.metadata.create_all(engine)

app = FastAPI(
    root_path=BASE_URL,
    docs_url= '/docs',
    redoc_url= '/redoc',
    openapi_url= '/openapi.json'
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# OAuth2 Dependency for as user item
async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(auth.oauth2_scheme), db : Session = Depends(get_db)) -> models.User | models.Bin : 
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    # Exception raised when the credentials are invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    # Exception raised when the scope is invalid
    scope_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value},
    )

    data = auth.get_data_from_token(token)
    
    if not data : raise credentials_exception
    username, scopes = data

    user = curd.get_user(db, username)
    bin = curd.get_bin(db, username)

    user = user if user else bin
    # Check if a valid user has been identified 
    if user is None:
        raise credentials_exception
    
    # verify if the token matches with the required requests
    for scope in security_scopes.scopes :
        if scope not in scopes :
            raise scope_exception
    return user


@app.get("/test")
async def index () :
    return {"message" : "Hello world from Money Plant"}

@app.get("/user/info", response_model=schemas.User )
def get_user (user: models.User = Security(get_current_user, scopes=[USER_TYPE]), db: Session = Depends(get_db)) : 
    return user

@app.post("/auth/register/user", response_model=schemas.UserBase)
def register_user (user:schemas.UserNew, db:Session = Depends(get_db)) :
    if  curd.get_user(db, email=user.email) : 
        raise HTTPException(status_code=400, detail="The given email id is already in use !")
    if curd.get_user_by_aadhaar(db, aadhaar=user.aadhaar) :
        raise HTTPException(status_code=400, detail="The aadhaar id is already registered !")
    if  not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", user.email):
        raise HTTPException(status_code=400, detail= "The given email id is invalid")
    curd.register_user(db, user)
    return curd.get_user(db, user.email)

@app.post("/auth/token", response_model=schemas.Token)
def login_user (form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) :
    user = curd.get_user(db, form.username)
    if user :
        if ( not auth.verify_password(user.password, form.password)) : raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Invalid credentials")
        return {"access_token": auth.create_access_token(user, USER_TYPE) , "token_type": "Bearer"}
    
    bin = curd.get_bin(db, form.username)
    if bin :
        if ( not auth.verify_password(bin.secret_key, form.password)) : raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Invalid credentials")
        return {"access_token": auth.create_access_token(bin, BIN_TYPE) , "token_type": "Bearer"}

@app.get("/user/transactions/all")
def get_all_transactions(user: models.User = Security(get_current_user, scopes=[USER_TYPE]), db:Session=Depends(get_db)):
    return {"transactions"  : curd.get_all_user_transaction(user_email=user.email) } 

@app.get("/user/bin/info", response_model=schemas.Bins)
def get_all_bins (user: models.User = Security(get_current_user, scopes=[USER_TYPE]), db: Session = Depends(get_db)) : 
    res = curd.get_all_bins(db)
    return {"bins" : res}

@app.post("/auth/register/bin", response_model=schemas.Bin)
def register_bin(new_bin:schemas.NewBin, db:Session=Depends(get_db)) :
    secret =  secrets.token_hex(32)
    bin = models.Bin(
        uid = uuid.uuid4().hex,
        secret_key = auth.hash_password(secret),
        address= new_bin.address,
        latitude= new_bin.latitude,
        longitude= new_bin.longitude
    )
    res =  curd.add_bin(db, bin)
    res.secret_key = secret
    return res

@app.get("/bin/info", response_model=schemas.BinBase )
def get_bin (bin: models.Bin  =Security(get_current_user, scopes=[BIN_TYPE]), db: Session = Depends(get_db)) :
    return bin

@app.get("/bin/user/info", response_model=schemas.User)
def get_user_info (email: str, bin: models.Bin = Security(get_current_user, scopes=[BIN_TYPE]), db:Session = Depends(get_db)):
    return curd.get_user(db, email)

@app.post("/bin/transaction/deposit", response_model=schemas.Transaction)
def deposit_transaction (
    transaction: schemas.TransactionBase,
    bin: models.Bin = Security(get_current_user, scopes=[BIN_TYPE]), 
    db:Session=Depends(get_db)) : 
    exception = HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid request")
    if transaction.bin_uid != bin.uid : raise exception
    if curd.get_waste_type(db, transaction.waste_type) == None : raise exception
    if curd.get_user(db, transaction.email) == None : raise exception
    
    return curd.add_transaction(db, transaction)

@app.get("/info/waste", response_model=schemas.WasteTypes)
def get_all_waste_types (user=Depends(get_current_user), db:Session = Depends(get_db)):
    return {"types" : curd.get_all_waste_types(db)}
    
    