from sqlalchemy.orm import Session


from .database import get_db, Base, engine
from .models import Bin

def add_bin (db: Session, password: str, lat: float, long: float ):
    db.add(bin)
    db.commit()
    db.close()


if __name__ == "__main__" :
    Base.metadata.create_all(engine)
    
    add_bin (
        get_db().__next__(),
        "JustLiving24",
        -25.344,
        131.031
    )