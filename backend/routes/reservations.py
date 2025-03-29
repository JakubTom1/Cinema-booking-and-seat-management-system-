from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Reservation
from backend.schemas import ReservationCreate

router = APIRouter()


@router.post("/")
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    existing_reservation = db.query(Reservation).filter_by(seat_number=reservation.seat_number).first()
    if existing_reservation:
        raise HTTPException(status_code=400, detail="Miejsce już zajęte!")

    new_reservation = Reservation(movie_id=reservation.movie_id, seat_number=reservation.seat_number)
    db.add(new_reservation)
    db.commit()
    return {"message": "Rezerwacja udana"}
