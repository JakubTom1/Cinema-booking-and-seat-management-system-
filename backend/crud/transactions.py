from sqlalchemy.orm import Session
from backend.models import Transaction, Ticket
from backend.schemas import TransactionCreate

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


def get_transactions_by_user(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.id_users == user_id).all()

def delete_transaction(db: Session, transaction: Transaction):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction.id).first()
    if db_transaction:
        # Delete associated tickets first
        db.query(Ticket).filter(Ticket.id_transaction == transaction.id).delete()
        db.delete(db_transaction)
        db.commit()
    return db_transaction
