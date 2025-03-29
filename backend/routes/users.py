from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Klient
from backend.schemas import UserCreate, UserResponse
import bcrypt

router = APIRouter()

# Endpoint do dodania nowego klienta
@router.post("/register")
def create_user(imie: str, nazwisko: str, login: str, haslo: str, db: Session = Depends(get_db)):
    db_klient = Klient(imie=imie, nazwisko=nazwisko, login=login, haslo=haslo)
    db.add(db_klient)
    db.commit()
    db.refresh(db_klient)
    return db_klient

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user