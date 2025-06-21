from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crud.tickets import create_tickets, get_tickets_by_transaction, ticket_info, delete_tickets
from backend.crud.transactions import create_transaction, realise_transaction, get_transactions_by_user
from backend.routes.auth import get_current_user
from backend.schemas import TicketCreate, TransactionCreate
from backend.database import get_db
from backend.models import Showing, Seat, Ticket, Pricelist
from typing import List
from datetime import timedelta
router = APIRouter()

@router.get("/reservations/{showing_id}")
def get_seats_for_showing(showing_id: int, db: Session = Depends(get_db)):
    # Krok 1: Znajdź seans
    showing = db.query(Showing).filter(Showing.id == showing_id).first()
    if not showing:
        raise HTTPException(status_code=404, detail="Showing not found")

    # Krok 2: Znajdź miejsca z sali przypisanej do seansu
    seats = db.query(Seat).filter(Seat.id_halls == showing.id_hall).all()

    # Krok 3: Dla każdego miejsca sprawdź, czy istnieje ticket z tym seat.id i showing_id
    results = []
    for seat in seats:
        is_taken = (
                db.query(Ticket)
                .join(Showing, Ticket.transaction.has(id_showings=Showing.id))
                .filter(
                    Ticket.id_seat == seat.id,
                    Showing.id == showing_id
                )
                .first() is not None
        )

        results.append({
            "seat_id": seat.id,
            "row": seat.row,
            "seat_num": seat.seat_num,
            "is_taken": is_taken
        })

    return results

@router.post("/transactions", response_model=dict)
def make_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = create_transaction(db, transaction)
    return {
        "transaction_id": db_transaction.id, 
        "status": db_transaction.status,
        "expires_at": (db_transaction.created_at + timedelta(minutes=15)).isoformat()
    }


@router.post("/tickets/bulk")
def reserve_tickets(tickets: List[TicketCreate], db: Session = Depends(get_db)):
    try:
        return create_tickets(db, tickets)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tickets/{transaction_id}")
def tickets_by_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return get_tickets_by_transaction(db, transaction_id)

@router.get("/ticket/{ticket_id}")
def get_ticket_info(ticket_id: int, db: Session = Depends(get_db)):
    return ticket_info(db, ticket_id)

@router.delete("/transactions/{transaction_id}/cancel")
def cancel_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Cancel a transaction by deleting all associated tickets and marking the transaction as cancelled.
    """
    return delete_tickets(db, transaction_id)

@router.get("/prices")
def get_ticket_prices(db: Session = Depends(get_db)):
    pricelist = db.query(Pricelist).all()
    if not pricelist:
        raise HTTPException(status_code=404, detail="No price list found")
    return pricelist

@router.put("/transactions/{transaction_id}")
def realise_transaction_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    return realise_transaction(db, transaction_id)

@router.get("/user/transactions")
def get_user_transactions(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    transactions = get_transactions_by_user(db, current_user)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user")
    return transactions