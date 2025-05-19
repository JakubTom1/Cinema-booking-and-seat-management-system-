from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from backend.schemas import UserCreate
from backend.crud.security import get_password_hash, get_current_user
from backend.models import User

# Sprawdzanie roli użytkownika
def admin_required(current_user: str = Depends(get_current_user)):
    db_user = get_user_by_login(current_user)
    if db_user.status != 0:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db_user

def staff_required(current_user: str = Depends(get_current_user)):
    db_user = get_user_by_login(current_user)
    if db_user.status > 1:
        raise HTTPException(status_code=403, detail="Staff access required")
    return db_user

# Pobieranie użytkownika po loginie
def get_user_by_login(login: str, db: Session):
    db_user = db.query(User).filter(User.login == login).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def create_user(db: Session, user: UserCreate):
    db_user = db.query(User).filter(User.login == user.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        password=hashed_password,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user