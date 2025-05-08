from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crud.tickets import delete_tickets
from backend.crud.transactions import delete_transaction
from backend.database import get_db
from backend.models import  Transaction

router = APIRouter()

@router.delete("/transactions/{transaction_id}")
def delete_transaction_and_tickets(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    try:
        delete_transaction(db, transaction)
        return {"message": f"Transaction {transaction_id} and related tickets deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting transaction: {str(e)}")
