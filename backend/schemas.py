"""
Moduł definiujący schematy Pydantic używane do walidacji danych wejściowych i wyjściowych.
"""

from pydantic import BaseModel, condecimal, EmailStr
from datetime import datetime
from typing import Optional, List

# Token schema
class Token(BaseModel):
    """
    Schemat reprezentujący token dostępu.
    """
    access_token: str
    token_type: str

# Schema for clients
class UserCreate(BaseModel):
    """
    Schemat danych wejściowych dla rejestracji użytkownika.
    """
    first_name: str
    last_name: str
    status: str
    login: str
    password: str

class UserResponse(BaseModel):
    """
    Schemat danych wyjściowych dla użytkownika.
    """
    id: int
    first_name: str
    last_name: str
    status: str
    login: str

    class Config:
        orm_mode = True

# Schema of movies
class MovieCreate(BaseModel):
    title: str

class Movie(MovieCreate):
    """
    Schemat danych wyjściowych dla filmu.
    """

    id: int

    class Config:
        orm_mode = True


# Schema of showing
class ShowingCreate(BaseModel):
    """
    Schemat danych wejściowych dla tworzenia nowego seansu filmowego.
    """
    id_movies: int
    date: datetime
    time: datetime
    id_hall: int

class ShowingSchema(ShowingCreate):
    """
        Schemat danych wyjściowych dla seansu filmowego.
        """
    id: int

# Schema of screening rooms
class HallCreate(BaseModel):
    """
    Schemat danych wejściowych dla tworzenia nowej sali kinowej.
    """
    hall_num: int
    seats_amount: int
    free_seats: int

class Hall(HallCreate):
    """
    Schemat danych wyjściowych dla sali kinowej.
    """
    id: int

    class Config:
        orm_mode = True


# Schema of places
class SeatCreate(BaseModel):
    """
    Schemat danych wejściowych dla tworzenia nowego miejsca w sali kinowej.
    """
    id_halls: int
    seat_num: int
    row: int
    occupied: bool

class ShowingResponse(BaseModel):
    """
    Schemat danych wyjściowych dla seansu filmowego, zawierający szczegóły filmu i sali.
    """
    id: int
    movie: Movie
    id_movies: int
    date: datetime
    time: datetime
    hall: Hall

    class Config:
        orm_mode = True

class Seat(SeatCreate):
    """
    Schemat danych wyjściowych dla miejsca w sali kinowej.
    """
    id: int

class SeatResponse(BaseModel):
    """
    Schemat danych wyjściowych dla miejsca w sali kinowej, zawierający dodatkowe informacje.
    """
    id: int
    seat_num: int
    row: int
    occupied: bool
    hall_id: int
    showing_id: Optional[int]

    class Config:
        orm_mode = True


# Schema of transactions
class TransactionCreate(BaseModel):
    """
    Schemat danych wejściowych dla tworzenia nowej transakcji (rezerwacji).
    """
    id_user: int
    amount: condecimal(max_digits=10, decimal_places=2)
    status: str
    date: datetime

class Transaction(TransactionCreate):
    """
    Schemat danych wyjściowych dla transakcji (rezerwacji).
    """
    id: int

class TransactionResponse(BaseModel):
    """
    Schemat danych wyjściowych dla transakcji, zawierający szczegóły miejsc.
    """
    id: int
    user_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    status: str
    date: datetime
    seats: List[SeatResponse]

    class Config:
        orm_mode = True


class GatesCreate(BaseModel):
    """
    Schemat danych wejściowych dla połączenia transakcji z miejscem.
    """
    id_transaction: int
    id_seats: int

class Gates(GatesCreate):
    """
    Schemat danych wyjściowych dla połączenia transakcji z miejscem.
    """
    id: int

    class Config:
        orm_mode = True
