from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True  # Pozwala na zwracanie obiektów SQLAlchemy jako JSON

class MovieCreate(BaseModel):
    title: str
    duration: int

class ReservationCreate(BaseModel):
    movie_id: int
    seat_number: str
