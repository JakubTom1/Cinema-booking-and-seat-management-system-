from fastapi import FastAPI
from database import Base, engine
from routes.users import router as users_router
from routes.reservations import router as reservations_router
from routes.movies import router as movies_router

# Tworzenie tabel w bazie danych (jeśli nie istnieją)
Base.metadata.create_all(bind=engine)

# Inicjalizacja FastAPI
app = FastAPI(title="System Rezerwacji Kinowej")

# Rejestrowanie endpointów z poszczególnych modułów
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(reservations_router, prefix="/reservations", tags=["Reservations"])
app.include_router(movies_router, prefix="/movies", tags=["Movies"])

# Endpoint testowy, by sprawdzić czy API działa
@app.get("/")
def read_root():
    return {"message": "Witaj w systemie rezerwacji kinowej!"}
