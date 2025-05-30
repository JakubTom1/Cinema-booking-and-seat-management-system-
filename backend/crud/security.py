from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional

SECRET_KEY = "4iGQqfT4ldocGxjftS-0WkN3mnZKCL8UdTOIB0rOFC6v7WpsKUnGzBudS1ZnvJ4v43HV99q2ckEiW8vw6DWsVQ"  # W produkcji użyj bezpiecznego klucza
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        status = payload.get("status")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
        return {'username': username, 'status': status}
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
