from sqlalchemy import Column, String, Integer, Table, Text, ForeignKey, Float, null
from sqlalchemy.orm import relationship

from .database import Base


class User (Base) : 
    __tablename__ = "users"
    email = Column(String(length=50), primary_key=True)
    name = Column(String(length=50), nullable=False)
    aadhaar_id = Column(String(length=12), nullable=False, unique=True)
    password = Column(String(length=64), nullable=False)
    credit_balance = Column(Float, default=0, nullable=False)

class Bin(Base) :
    __tablename__ = "bins"
    uid = Column(String(length=36), primary_key=True)
    secret_key = Column(String(length=64))
    address = Column(String(length=200), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    fill_level = Column(Float, nullable=False, default=0.0)
    # State values correspond to the availability of the bin
    # State = -1 (Bin is awaiting to be serviced)
    # State = 0 (Bin is offline)
    # State = 1 (Bin is active and enabled)
    state = Column(Integer, nullable=False, default=0)

class WasteType (Base) : 
    __tablename__ = "waste_types"
    type = Column(String(length=20), primary_key=True)
    credits = Column(Float, nullable=False)


class Transaction (Base) :
    __tablename__ = "transactions"
    uid = Column(String(length=36), primary_key=True)
    email = Column(String(length=50), ForeignKey("users.email"), nullable=False)
    bin_uid = Column(String(length=36), ForeignKey("bins.uid"), nullable=False)
    waste_type = Column(String(length=20), ForeignKey("waste_types.type"), nullable=False)
    weight = Column(Float, nullable=False)
    credits = Column(Float, nullable=False)

