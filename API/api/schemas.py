from typing import List
from pydantic import BaseModel

class UserBase (BaseModel) :
    email : str
    class Config :
        orm_mode = True

#Schema to authenticate a user
class UserAuth (UserBase) :
    password : str

# Schema to create a new user
class UserNew (UserAuth) :
    name : str
    aadhaar : str

# Schema to return User Information
class User (UserBase) :
    name : str
    aadhaar_id : str
    credit_balance : int

#Schema for new bin creation 
class NewBin(BaseModel):
    latitude: float
    longitude: float 
    address: str

# Schema to relay info about the bin
class BinBase (BaseModel) :
    uid: str
    latitude: float
    longitude: float
    address: str
    fill_level: float
    state: int
    class Config :
        orm_mode = True

class Bin (BinBase) : 
    secret_key : str

class Bins (BaseModel) :
    bins : List[BinBase]
    class Config :
        orm_mode = True

# Schemas for transactional Information
class TransactionBase (BaseModel) : 
    email: str
    bin_uid: str
    waste_type: str
    weight: float
    class Config :
        orm_mode = True

class Transaction (TransactionBase) : 
    uid: str
    credits: str
    class Config :
        orm_mode = True

class Transactions (BaseModel) :
    transactions : List[Transaction]
    class Config  :
        orm_mode = True

class WasteCredit (BaseModel):
    type: str
    credits: float
    class Config: 
        orm_mode = True

class WasteTypes (BaseModel) : 
    types : List[WasteCredit]

# Schema for the authentication token
class Token (BaseModel):
    access_token : str
    token_type : str


