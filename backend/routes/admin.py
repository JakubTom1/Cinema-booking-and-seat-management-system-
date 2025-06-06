from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session
from backend.crud.admin import create_showing, delete_showing, check_showing_time_difference
from backend.schemas import ShowingCreate
from backend.database import get_db
from backend.models import Showing

router = APIRouter()

@router.post("/admin/showings")
def admin_add_showing(showing: ShowingCreate, db: Session = Depends(get_db)):
    if not check_showing_time_difference(db, showing):
        raise HTTPException(status_code=400, detail="The time difference between showings is less than 3 hours.")
    return create_showing(db, showing)

@router.delete("/admin/showings/{showing_id}")
def admin_remove_showing(showing_id: int, db: Session = Depends(get_db)):
    showing = db.query(Showing).filter(Showing.id == showing_id).first()
    if not showing:
        raise HTTPException(status_code=404, detail="Showing not found")
    return delete_showing(db, showing_id)
