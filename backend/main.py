from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Klient, Film, Seans, Sala, Miejsce, Transakcja
from schemas import KlientCreate, FilmCreate, SeansCreate, SalaCreate, MiejsceCreate, TransakcjaCreate

# Initialize database
init_db()

app = FastAPI()

# Funkcja do pozyskiwania sesji
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpointy API do obsługi różnych zasobów (np. Klientów, Filmów, Seansów)

@app.post("/klienci/", response_model=Klient)
def create_klient(klient: KlientCreate, db: Session = Depends(get_db)):
    db_klient = Klient(imie=klient.imie, nazwisko=klient.nazwisko, login=klient.login, haslo=klient.haslo)
    db.add(db_klient)
    db.commit()
    db.refresh(db_klient)
    return db_klient

@app.post("/filmy/", response_model=Film)
def create_film(film: FilmCreate, db: Session = Depends(get_db)):
    db_film = Film(tytul=film.tytul, grany_od=film.grany_od, grany_do=film.grany_do)
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film

# Można dodać więcej endpointów dla Seansów, Sal, Miejsc i Transakcji
