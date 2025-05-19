'''from fastapi import APIRouter, Depends
from backend.database import engine
from sqlalchemy import text
from backend.middleware.auth_middleware import admin_required

router = APIRouter()

@router.get("/reports/earnings", dependencies=[Depends(admin_required)])
def report_earnings():
    query = """
        SELECT m.tittle, COUNT(t.id) AS sold_tickets, SUM(p.ticket_price) AS total_earnings
        FROM tickets t
        JOIN transactions tr ON t.id_transaction = tr.id
        JOIN showings s ON tr.id_showings = s.id
        JOIN movies m ON s.id_movies = m.id
        JOIN pricelist p ON t.id_pricelist = p.id
        GROUP BY m.tittle
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]

@router.get("/reports/occupancy", dependencies=[Depends(admin_required)])
def report_occupancy():
    query = """
        SELECT s.id, m.tittle, 
               COUNT(t.id) as sold_seats,
               h.seats_amount as total_seats,
               (COUNT(t.id) * 100.0 / h.seats_amount) as occupancy_rate
        FROM showings s
        JOIN movies m ON s.id_movies = m.id
        JOIN halls h ON s.id_hall = h.id
        LEFT JOIN transactions tr ON s.id = tr.id_showings
        LEFT JOIN tickets t ON tr.id = t.id_transaction
        GROUP BY s.id, m.tittle, h.seats_amount
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]'''
