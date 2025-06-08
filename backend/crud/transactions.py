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

def realise_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db_transaction.status = "realized"
        db.commit()
        return db_transaction
    return None

def get_transactions_by_user(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.id_users == user_id).all()
