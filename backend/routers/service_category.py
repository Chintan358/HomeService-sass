from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_password_hash
from ..models.service_category import ServiceCategory
from ..models.user import UserRole
from ..schemas.service_category import (
    ServiceCategoryCreate,
    ServiceCategoryUpdate,
    ServiceCategoryOut,
)
from ..utils.dependencies import get_current_user

router = APIRouter()

def _require_superadmin(user = Depends(get_current_user)):
    if user.role != UserRole.superadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return user

@router.post("/", response_model=ServiceCategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: ServiceCategoryCreate,
    db: Session = Depends(get_db),
    _: None = Depends(_require_superadmin),
):
    existing = db.query(ServiceCategory).filter(ServiceCategory.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = ServiceCategory(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/", response_model=list[ServiceCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(ServiceCategory).all()

@router.get("/{category_id}", response_model=ServiceCategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router.put("/{category_id}", response_model=ServiceCategoryOut)
def update_category(
    category_id: int,
    payload: ServiceCategoryUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(_require_superadmin),
):
    cat = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(_require_superadmin),
):
    cat = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return None
