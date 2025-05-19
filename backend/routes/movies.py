from fastapi import APIRouter
from backend.database import engine
from sqlalchemy import text

router = APIRouter()

@router.get("/movies/{id_movies}")
def get_movies():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM movies"))
        return [dict(row._mapping) for row in result]
