from sqlalchemy.orm import Session
from backend.models import Showing, Calendar, Movie
from backend.schemas import ShowingCreate, ShowingRead

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

from datetime import datetime
def check_showing_time_difference(db: Session, showing: ShowingRead):
    existing_showings = db.query(Showing).filter(
        Showing.id_date == showing.id_date,
        Showing.id_hall == showing.id_hall
    ).all()

    if not existing_showings:
        return True

    dummy_date = datetime.now().replace(tzinfo=None).date()

    for existing_showing in existing_showings:
        existing_time = existing_showing.hour.replace(tzinfo=None)
        showing_time = showing.hour.replace(tzinfo=None)

        existing_dt = datetime.combine(dummy_date, existing_time)
        showing_dt = datetime.combine(dummy_date, showing_time)

        time_difference_minutes = abs((existing_dt - showing_dt).total_seconds()) / 60

        if time_difference_minutes < 180:
            return False

    return True

def delete_showing(db: Session, showing_id: int):
    db_showing = db.query(Showing).filter(Showing.id == showing_id).first()
    if db_showing:
        db.delete(db_showing)
        db.commit()
        return True
    return False