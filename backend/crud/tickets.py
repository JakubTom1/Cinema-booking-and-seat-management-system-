from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, text
from fastapi import HTTPException
from backend.models import Ticket, Transaction
from backend.schemas import TicketCreate
from typing import List

def is_seat_available(db: Session, seat_id: int, showing_id: int) -> bool:
    existing_ticket = (
        db.query(Ticket)
        .join(Transaction, Ticket.id_transaction == Transaction.id)
        .filter(and_(
            Ticket.id_seat == seat_id,
            Transaction.id_showings == showing_id
        ))
        .first()
    )
    return existing_ticket is None

def create_tickets(db: Session, tickets: List[TicketCreate]):
    if not tickets:
        raise HTTPException(status_code=400, detail="No tickets provided")

    transaction_id = tickets[0].id_transaction
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    try:
        db.execute(text("SELECT * FROM transactions WHERE id = :id FOR UPDATE NOWAIT"), {"id": transaction_id})
    except Exception:
        raise HTTPException(status_code=409, detail="Another transaction is in progress")

    created_tickets = []
    for ticket in tickets:
        if not is_seat_available(db, ticket.id_seats, transaction.id_showings):
            raise HTTPException(status_code=409, detail=f"Seat {ticket.id_seats} already booked")

        db_ticket = Ticket(
            id_transaction=transaction_id,
            id_pricelist=ticket.id_pricelist,
            id_seat=ticket.id_seats
        )
        db.add(db_ticket)
        created_tickets.append(db_ticket)

    try:
        db.commit()
        for t in created_tickets:
            db.refresh(t)
        return created_tickets
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while booking tickets")


def get_tickets_by_transaction(db: Session, transaction_id: int):
    # Retrieve all tickets associated with the given transaction ID
    return db.query(Ticket).filter(Ticket.id_transaction == transaction_id).all()