from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for clients
class KlientCreate(BaseModel):
    imie: str
    nazwisko: str
    login: str
    haslo: str

class Klient(KlientCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of movies
class FilmCreate(BaseModel):
    tytul: str
    grany_od: datetime
    grany_do: datetime

class Film(FilmCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of showing
class SeansCreate(BaseModel):
    id_film: int
    data: datetime
    godzina: datetime
    id_sala: int

class Seans(SeansCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of screening rooms
class SalaCreate(BaseModel):
    liczba_miejsc: int
    liczba_wolnych_miejsc: int

class Sala(SalaCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of places
class MiejsceCreate(BaseModel):
    numer_miejsca: int
    czy_wolne: bool
    id_sali: int

class Miejsce(MiejsceCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of transactions
class TransakcjaCreate(BaseModel):
    id_klienta: int
    kwota: float
    status: str
    data: datetime

class Transakcja(TransakcjaCreate):
    id: int

    class Config:
        orm_mode = True
