from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import TicketRead
from backend.crud.tickets import delete_tickets
from backend.routes.auth import get_current_user
router = APIRouter()


@router.delete("/tickets/", response_model=dict)
async def delete_tickets_endpoint(
        tickets: List[TicketRead],
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    """
    Delete tickets and cancel associated transaction.

    Args:
        tickets: List of tickets to delete
        db: Database session

    Returns:
        Message confirming deletion
    """
    if current_user.get("status") > 0:
        raise HTTPException(status_code=403, detail="Stuff access required")
    try:
        result = delete_tickets(db=db, tickets=tickets)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting tickets: {str(e)}"
        )
