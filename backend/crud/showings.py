from sqlalchemy.orm import Session
from backend.models import Showing, Calendar, Movie
from backend.schemas import ShowingCreate
from datetime import datetime, timedelta

def create_showing(db: Session, showing: ShowingCreate):
    db_showing = Showing(
        id_movies=showing.id_movies,
        id_hall=showing.id_hall,
        id_date=showing.id_date,
        hour=showing.hour
    )
    db.add(db_showing)
    db.commit()
    db.refresh(db_showing)
    return db_showing


def delete_showing(db: Session, showing_id: int):
    db_showing = db.query(Showing).filter(Showing.id == showing_id).first()
    if db_showing:
        db.delete(db_showing)
        db.commit()
    return db_showing


def get_showings_by_date(db: Session, date_id: int):
    return db.query(Showing).filter(Showing.id_date == date_id).all()

def current_showings(db: Session):
    today = datetime.today()
    next_week = today + timedelta(days=6)

    showings = (
        db.query(Showing)
        .join(Calendar, Showing.id_date == Calendar.id)
        .join(Movie, Showing.id_movies == Movie.id)
        .filter(Calendar.date >= today, Calendar.date <= next_week)
        .order_by(Calendar.date, Showing.hour)
        .all()
    )
    return showings