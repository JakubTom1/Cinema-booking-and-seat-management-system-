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


def check_showing_time_difference(db: Session, showing: ShowingRead):
    existing_showings = db.query(Showing).filter(
        Showing.id_date == showing.id_date,
        Showing.id_hall == showing.id_hall
    ).all()
    if not existing_showings:
        return True

    for existing_showing in existing_showings:
        time_difference = abs(existing_showing.hour - showing.hour)
        if time_difference < 3:
            return False

    return True

def delete_showing(db: Session, showing_id: int):
    db_showing = db.query(Showing).filter(Showing.id == showing_id).first()
    if db_showing:
        db.delete(db_showing)
        db.commit()
        return True
    return False