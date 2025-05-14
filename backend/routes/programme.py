from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.database import get_db
from backend.models import Showing, Calendar, Movie
from backend.crud.showings import current_showings
router = APIRouter()
print("programme router loaded")

@router.get("/programme")
def get_week_programme(db: Session = Depends(get_db)):
    try:
        showings = current_showings(db)
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
