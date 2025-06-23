from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.models import Transaction, Ticket, User
from backend.schemas import TransactionCreate
from fastapi import HTTPException
from datetime import datetime, timedelta

def create_transaction(db: Session, transaction: TransactionCreate):
    # Usuń przeterminowane transakcje przed utworzeniem nowej
    cleanup_expired_transactions(db)
    
    db_transaction = Transaction(
        id_users=transaction.id_users,
        id_showings=transaction.id_showings,
        status="pending",
        date=transaction.date,
        created_at=datetime.now()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def cleanup_expired_transactions(db: Session):
    """Usuwa transakcje starsze niż 15 minut ze statusem 'pending'"""
    expiry_time = datetime.now() - timedelta(minutes=15)
    
    # Usuń bilety powiązane z przeterminowanymi transakcjami
    db.execute(text("""
        DELETE t FROM tickets t
        INNER JOIN transactions tr ON t.id_transaction = tr.id
        WHERE tr.status = 'pending' AND tr.created_at < :expiry_time
    """), {"expiry_time": expiry_time})
    
    # Usuń przeterminowane transakcje
    db.execute(text("""
        DELETE FROM transactions 
        WHERE status = 'pending' AND created_at < :expiry_time
    """), {"expiry_time": expiry_time})
    
    db.commit()

def realise_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db_transaction.status = "realized"
        db.commit()
        return db_transaction
    return None

def get_transactions_by_user(db: Session, current_user: dict):
    username = current_user.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Pobieramy użytkownika z bazy danych
    user = db.query(User).filter(User.login == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Pobieramy transakcje użytkownika
    transactions = db.query(Transaction).filter(Transaction.id_users == user.id).all()

    results = []
    for transaction in transactions:
        showing = transaction.showing
        movie = showing.movie
        calendar = showing.calendar
        hall = showing.hall
        tickets = transaction.tickets
        ticket_data = []
        for ticket in tickets:
            seat = ticket.seat
            pricelist = ticket.pricelist
            ticket_data.append({
                "seat_row": seat.row,
                "seat_number": seat.seat_num,
                "price": float(pricelist.ticket_price)
            })

        results.append({
            "transaction_id": transaction.id,
            "status": transaction.status,
            "movie_title": movie.tittle,
            "date": calendar.date.date(),  # data
            "time": showing.hour,  # godzina seansu
            "hall_number": hall.hall_num,
            "transaction_date": transaction.date,
            "seats": [{"row": t["seat_row"], "number": t["seat_number"]} for t in ticket_data],
            "total_price": sum(t["price"] for t in ticket_data)
        })

    return results