from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import date
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import BetaTester

router = APIRouter()

class BetaTesterCreate(BaseModel):
    email: EmailStr
    name: str
    dob: date

@router.post("/signup")
def create_beta_tester(tester: BetaTesterCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(BetaTester).filter(BetaTester.email == tester.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="You’ve already signed up.")

    new_tester = BetaTester(
        email=tester.email,
        name=tester.name,
        dob=tester.dob,
    )
    db.add(new_tester)
    db.commit()
    db.refresh(new_tester)
    return {"message": "Thanks for signing up!"}