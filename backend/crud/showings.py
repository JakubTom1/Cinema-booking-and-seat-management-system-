from sqlalchemy.orm import Session
from backend.models import Showing
from backend.schemas import ShowingCreate


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