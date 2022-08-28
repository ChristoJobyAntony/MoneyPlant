import json
import secrets
from typing import Dict, List
from uuid import uuid4
from api.auth import hash_password
from api.models import Bin, User
from api.database import get_db
from sqlalchemy.orm import Session


def run_first_commit() :

    db : Session = get_db().__next__()

    user = User(
        email="christotantony2003@gmail.com",
        name="Christo",
        aadhaar_id="123456789012",
        password=hash_password("Tony*2003"),
        credit_balance="0.00"
    )

    bin = Bin(
        uid="726dcba2ae4247839632a9eb521a24b5",
        secret_key="$12$15kwXHTF1ZDLY50BRVExqOPOtROf77ZjPnh39OXxv.GlQFE0.HW32",
        address="VIT Chennai, Near Food Stall",
        latitude=12.8414,
        longitude=80.1540,
        state=0
    )

    # Add filler data
    bins = []
    with open("./api/data.json") as f :
        dat : Dict[str, List]= json.load(f)
        for val in dat.values() :
            print("Adding bin "+val[0])
            bins.append(
                Bin(
                    uid=uuid4().hex,
                    secret_key=hash_password(secrets.token_hex(32)),
                    latitude=val[2],
                    longitude=val[1],
                    address=val[0],
                    state=0
                )
            )

    if bin : db.add(bin)
    if user : db.add(user)
    db.add_all(bins)
    db.commit()
