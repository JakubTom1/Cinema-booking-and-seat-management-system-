from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema dla Klienta
class KlientCreate(BaseModel):
    imie: str
    nazwisko: str
    login: str
    haslo: str

class Klient(KlientCreate):
    id: int

    class Config:
        orm_mode = True


# Schema dla Filmu
class FilmCreate(BaseModel):
    tytul: str
    grany_od: datetime
    grany_do: datetime

class Film(FilmCreate):
    id: int

    class Config:
        orm_mode = True


# Schema dla Seansu
class SeansCreate(BaseModel):
    id_film: int
    data: datetime
    godzina: datetime
    id_sala: int

class Seans(SeansCreate):
    id: int

    class Config:
        orm_mode = True


# Schema dla Sali
class SalaCreate(BaseModel):
    liczba_miejsc: int
    liczba_wolnych_miejsc: int

class Sala(SalaCreate):
    id: int

    class Config:
        orm_mode = True


# Schema dla Miejsca
class MiejsceCreate(BaseModel):
    numer_miejsca: int
    czy_wolne: bool
    id_sali: int

class Miejsce(MiejsceCreate):
    id: int

    class Config:
        orm_mode = True


# Schema dla Transakcji
class TransakcjaCreate(BaseModel):
    id_klienta: int
    kwota: float
    status: str
    data: datetime

class Transakcja(TransakcjaCreate):
    id: int

    class Config:
        orm_mode = True
