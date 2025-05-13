'''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.middleware.auth_middleware import admin_required
from backend.crud.showings import create_showing, delete_showing
from backend.schemas import ShowingCreate
from backend.database import get_db

router = APIRouter()

@router.post("/admin/showings")
def admin_add_showing(showing: ShowingCreate, db: Session = Depends(get_db), 
                     _: dict = Depends(admin_required)):
    return create_showing(db, showing)

@router.delete("/admin/showings/{showing_id}")
def admin_remove_showing(showing_id: int, db: Session = Depends(get_db), 
                        _: dict = Depends(admin_required)):
    return delete_showing(db, showing_id)'''
