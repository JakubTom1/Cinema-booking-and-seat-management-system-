from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.database import get_db
from backend.models import Showing, Calendar, Movie
router = APIRouter()
print("programme router loaded")

@router.get("/programme")
def get_week_programme(db: Session = Depends(get_db)):
    try:
        today = datetime.today()
        next_week = today + timedelta(days=7)

        showings = (
            db.query(Showing)
            .join(Calendar, Showing.id_date == Calendar.id)
            .join(Movie, Showing.id_movies == Movie.id)
            .filter(Calendar.date >= today, Calendar.date <= next_week)
            .order_by(Calendar.date, Showing.hour)
            .all()
        )

        result = []
        for showing in showings:
            result.append({
                "date": showing.calendar.date.strftime("%Y-%m-%d"),
                "time": showing.hour.strftime("%H:%M"),
                "movie_title": showing.movie.tittle
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
