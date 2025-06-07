'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sqlalchemy import text
from typing import List
import models, schemas
from database import get_db

# Tworzenie aplikacji FastAPI
app = FastAPI()

# Dodaj CORS middleware
# Fast Api działa na 8000, a tutaj dostaje dostęp do portu na którym działą strona
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # Zezwól na dostęp z tego portu
    allow_credentials=True,
    allow_methods=["*"],  # Zezwól na wszystkie metody (GET, POST itd.)
    allow_headers=["*"],  # Zezwól na wszystkie nagłówki
)

def json_maker(query:str):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        movies = [dict(row._mapping) for row in result]
    return movies

@app.get("/movies", response_model=List[schemas.MovieRead])
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    # query all movies
    return movies

@app.get("/week")
def get_week():
    query =(
        """
        select weekday(c.date)
        from calendar as c
        where c.date >= curdate()
        order by c.date asc
        limit 7
        """
    )
    # query the newest week days
    return json_maker(query)

@app.get("/pricelist")
def get_prices():
    query =(
        """
        select p.type, p.ticket_price
        from pricelist as p
        """
    )
    return json_maker(query)



"""
Główny moduł aplikacji FastAPI, definiujący endpointy API.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, date as DateType
from database import init_db, get_db
from models import User, Movie, Hall, Seat, Gate, Showing, Transaction
from schemas import *
from fastapi.middleware.cors import CORSMiddleware
from auth import *
from fastapi.security import OAuth2PasswordRequestForm
from api_docs import API_TAGS

# Inicjalizacja bazy danych
init_db()

# Tworzenie instancji aplikacji FastAPI
app = FastAPI(
    title="Cinema Booking System",
    description="API for cinema booking and seat management system",
    version="1.0.0",
    openapi_tags=API_TAGS
)

# Konfiguracja CORS
origins = ["http://localhost:3000", "http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movies/{date}", response_model=list[ShowingResponse], tags=["movies"])
def get_movies_by_date(date: DateType, db: Session = Depends(get_db)):
    """
    Pobiera wszystkie seanse filmowe dla podanej daty.
    """
    showings = db.query(Showing).filter(Showing.date == date).all()
    if not showings:
        raise HTTPException(status_code=404, detail="No showings found for this date")
    return showings

@app.get("/seats/{showing_id}", response_model=list[SeatResponse], tags=["seats"])
def get_seats_for_showing(showing_id: int, db: Session = Depends(get_db)):
    """
    Pobiera wszystkie miejsca dla konkretnego seansu.
    """
    seats = db.query(Seat).join(Hall).join(Showing).filter(Showing.id == showing_id).all()
    return seats

@app.post("/reservations/", response_model=TransactionResponse, tags=["reservations"])
def create_reservation(reservation: TransactionCreate, db: Session = Depends(get_db)):
    """
    Tworzy nową rezerwację na podstawie przesłanych danych.
    """
    new_transaction = Transaction(**reservation.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@app.post("/register", response_model=UserResponse, tags=["users"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Rejestruje nowego użytkownika w systemie.
    """
    db_user = User(
        login=user.login,
        password=get_password_hash(user.password),
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token, tags=["auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Loguje użytkownika i generuje token dostępu.
    """
    user = db.query(User).filter(User.login == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserResponse, tags=["users"])
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Pobiera informacje o aktualnie zalogowanym użytkowniku.
    """
    return current_user
    '''

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.routes import auth, movies, showings, reservations, admin, reports, programme, delete_ticket
from backend.routes.auth import get_current_user
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342", "http://127.0.0.1:5500", "http://127.0.0.2:5501"],  # Zezwól na dostęp z tego portu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(showings.router, prefix="/showings", tags=["Showings"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"], dependencies=[Depends(get_current_user)])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
#app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(programme.router, prefix = "", tags=["Programme"])
app.include_router(delete_ticket.router, prefix = "", tags = ["Delete Ticket"], dependencies=[Depends(get_current_user)])


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Cinema booking API is running."}



