from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas import UserCreate
from backend.crud.security import get_password_hash, verify_password
from backend.models import User

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.login == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user