from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas import UserCreate
from backend.crud.security import get_password_hash, verify_password
from backend.models import User


# Sprawdzanie roli użytkownika
def admin_required(current_user: str = Depends()):
    db_user = get_user_by_login(current_user)
    if db_user.status != 0:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db_user

def staff_required(current_user: str = Depends()):
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

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.login == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user