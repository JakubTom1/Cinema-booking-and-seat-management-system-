"""
Moduł odpowiedzialny za uwierzytelnianie i autoryzację użytkowników.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.crud.users import get_user_by_login, create_user
from backend.crud.security import verify_password, create_access_token, get_current_user
from backend.schemas import Token, UserCreate, UserRead
from backend.models import User

router = APIRouter()

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_login(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/users/{login}", response_model=UserRead)
def get_user_by_login_endpoint(login: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_user = get_user_by_login(login, db)
    return db_user


'''
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import Token

# Konfiguracja haszowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Konfiguracja OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Klucz i algorytm JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Weryfikuje, czy podane hasło jest zgodne z zahaszowanym hasłem.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Haszuje podane hasło.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Tworzy token dostępu JWT z podanymi danymi i czasem wygaśnięcia.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Pobiera aktualnie zalogowanego użytkownika na podstawie tokenu JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.login == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
'''