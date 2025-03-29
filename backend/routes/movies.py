from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Movie
from backend.schemas import MovieCreate

router = APIRouter()

@router.get("/")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.post("/")
def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    new_movie = Movie(title=movie.title, duration=movie.duration)
    db.add(new_movie)
    db.commit()
    return {"message": "Film dodany!"}
