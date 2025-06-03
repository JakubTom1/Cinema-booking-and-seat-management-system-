from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.crud.showings import create_showing, delete_showing, get_showings_by_date, get_movie_by_id
from backend.schemas import ShowingCreate
from backend.database import get_db
router = APIRouter()

@router.get("/movies/{id_movies}")
def get_movies(id_movies : int, db: Session = Depends(get_db)):
    return get_movie_by_id(db, id_movies)

