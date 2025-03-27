from fastapi import FastAPI, Depends
from database import SessionLocal
from models import Reservation

app = FastAPI()

@app.get("/seanse")
def get_seanse():
    return [{"title": "Incepcja", "id": 1}, {"title": "Interstellar", "id": 2}]

@app.post("/rezerwuj")
def rezerwuj_seans(seans_id: int, miejsce: str):
    return {"message": "Rezerwacja udana"}