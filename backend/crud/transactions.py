from sqlalchemy.orm import Session
from backend.models import Transaction, Ticket, User
from backend.schemas import TransactionCreate
from fastapi import HTTPException

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(
        id_users=transaction.id_users,
        id_showings=transaction.id_showings,
        status=transaction.status,
        date=transaction.date
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

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
            "seats": [{"row": t["seat_row"], "number": t["seat_number"]} for t in ticket_data],
            "total_price": sum(t["price"] for t in ticket_data)
        })

    return results