from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.technician import Technician
from ..models.user import User, UserRole
from ..schemas.technician import TechnicianCreate, TechnicianUpdate, TechnicianOut
from ..utils.dependencies import get_current_user

router = APIRouter()

def _require_superadmin(user: User = Depends(get_current_user)):
    if user.role != UserRole.superadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Superadmin required")
    return user

def _require_provider(user: User = Depends(get_current_user)):
    if user.role != UserRole.provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provider required")
    return user

@router.post("/", response_model=TechnicianOut, status_code=status.HTTP_201_CREATED)
def create_technician(
    payload: TechnicianCreate,
    db: Session = Depends(get_db),
    _: User = Depends(_require_provider),
):
    # Ensure the linked user exists and is a technician role (could be validated elsewhere)
    existing = db.query(Technician).filter(Technician.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Technician already exists for this user")
    tech = Technician(**payload.dict())
    db.add(tech)
    db.commit()
    db.refresh(tech)
    return tech

@router.get("/", response_model=list[TechnicianOut])
def list_technicians(db: Session = Depends(get_db), _: User = Depends(_require_superadmin)):
    return db.query(Technician).all()

@router.get("/{tech_id}", response_model=TechnicianOut)
def get_technician(tech_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tech = db.query(Technician).filter(Technician.id == tech_id).first()
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")
    # Providers can see their own techs; superadmin can see all
    if user.role == UserRole.provider and tech.provider_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if user.role not in (UserRole.superadmin, UserRole.provider):
        raise HTTPException(status_code=403, detail="Access denied")
    return tech

@router.put("/{tech_id}", response_model=TechnicianOut)
def update_technician(
    tech_id: int,
    payload: TechnicianUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(_require_provider),
):
    tech = db.query(Technician).filter(Technician.id == tech_id).first()
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(tech, field, value)
    db.commit()
    db.refresh(tech)
    return tech

@router.delete("/{tech_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technician(
    tech_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(_require_superadmin),
):
    tech = db.query(Technician).filter(Technician.id == tech_id).first()
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")
    db.delete(tech)
    db.commit()
    return None
