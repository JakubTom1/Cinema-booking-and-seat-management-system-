from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.crud.security import create_access_token, get_password_hash, get_user
from backend.crud.users import authenticate_user
from backend.models import User
from backend.schemas import UserCreate, UserResponse, Token
from datetime import timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Sprawdzenie czy użytkownik już istnieje
    db_user = db.query(User).filter(User.login == user.login).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    # Utworzenie nowego użytkownika
    hashed_password = get_password_hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        password=hashed_password,
        status=2  # domyślnie klient
    )
    print(db_user)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)

    # Utworzenie tokenu
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login, "status": user.status},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_status": user.status
    }

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Funkcja pomocnicza do pobierania aktualnego użytkownika na podstawie tokenu.
    """
    user = get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user