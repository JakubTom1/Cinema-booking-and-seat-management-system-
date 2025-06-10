from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime
from decimal import Decimal

# input schemas

# USER
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    login: str
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    login: str
    status: int

    class Config:
        orm_mode = True



# MOVIE
class MovieCreate(BaseModel):
    tittle: str


# PRICELIST
class PricelistCreate(BaseModel):
    type: str
    ticket_price: Decimal


# CALENDAR
class CalendarCreate(BaseModel):
    date: datetime


# HALL
class HallCreate(BaseModel):
    hall_num: int
    seats_amount: int


# SEAT
class SeatCreate(BaseModel):
    id_halls: int
    seat_num: int
    row: int


# SHOWING
class ShowingCreate(BaseModel):
    id_movies: int
    id_hall: int
    id_date: int
    hour: time


# TRANSACTION
class TransactionCreate(BaseModel):
    id_users: int
    id_showings: int
    status: str
    date: date


# TICKET
class TicketCreate(BaseModel):
    id_transaction: int
    id_pricelist: int
    id_seats: int

# output schemas

# USER
class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    status: int
    login: str

    class Config:
        orm_mode = True


# MOVIE
class MovieRead(BaseModel):
    id: int
    tittle: str

    class Config:
        orm_mode = True


# PRICELIST
class PricelistRead(BaseModel):
    id: int
    type: str
    ticket_price: Decimal

    class Config:
        orm_mode = True


# CALENDAR
class CalendarRead(BaseModel):
    id: int
    date: datetime

    class Config:
        orm_mode = True


# HALL
class HallRead(BaseModel):
    id: int
    hall_num: int
    seats_amount: int

    class Config:
        orm_mode = True


# SEAT
class SeatRead(BaseModel):
    id: int
    id_halls: int
    seat_num: int
    row: int

    class Config:
        orm_mode = True


# SHOWING
class ShowingRead(BaseModel):
    id: int
    id_movies: int
    id_hall: int
    id_date: int
    hour: time

    class Config:
        orm_mode = True


# TRANSACTION
class TransactionRead(BaseModel):
    id: int
    id_users: int
    id_showings: int
    status: str
    date: date

    class Config:
        orm_mode = True


# TICKET
class TicketRead(BaseModel):
    id: int
    id_transaction: int
    id_pricelist: int
    id_seats: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_status: int
    user_id: int

class TokenData(BaseModel):
    username: str | None = None
    status: int | None = None