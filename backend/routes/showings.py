from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.crud.showings import create_showing, delete_showing, get_showings_by_date
from backend.schemas import ShowingCreate
from backend.database import get_db

router = APIRouter()
@router.get("/showings/by-date/{date_id}")
def showings_by_date(date_id: int, db: Session = Depends(get_db)):
    return get_showings_by_date(db, date_id)

@router.post("/showings")
def add_showing(showing: ShowingCreate, db: Session = Depends(get_db)):
    return create_showing(db, showing)

@router.delete("/showings/{showing_id}")
def remove_showing(showing_id: int, db: Session = Depends(get_db)):
    return delete_showing(db, showing_id)


