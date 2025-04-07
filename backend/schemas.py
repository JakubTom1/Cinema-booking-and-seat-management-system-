from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional

# Schema for clients
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    status : str
    login: str
    password: str

class User(UserCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of movies
class MovieCreate(BaseModel):
    title: str

class Movie(MovieCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of showing
class ShowingCreate(BaseModel):
    id_movies: int
    date: datetime
    time: datetime
    id_hall: int

class Showing(ShowingCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of screening rooms
class HallCreate(BaseModel):
    hall_num: int
    seats_amount: int
    free_seat: int

class Hall(HallCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of places
class SeatCreate(BaseModel):
    id_halls: int
    seat_num: int
    row: int
    occupied: bool


class Seat(SeatCreate):
    id: int

    class Config:
        orm_mode = True


# Schema of transactions
class TransactionCreate(BaseModel):
    id_user: int
    amount: condecimal(max_digits=10, decimal_places=2)
    status: str
    date: datetime

class Transaction(TransactionCreate):
    id: int

    class Config:
        orm_mode = True


class GatesCreate(BaseModel):
    id_transaction: int
    id_seats: int

class Gates(GatesCreate):
    id: int

    class Config:
        orm_mode = True