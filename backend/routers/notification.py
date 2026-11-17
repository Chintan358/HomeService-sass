from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.notification import Notification
from ..models.user import User, UserRole
from ..schemas.notification import NotificationCreate, NotificationOut, NotificationReadUpdate
from ..utils.dependencies import get_current_user

router = APIRouter()

def _require_superadmin(user: User = Depends(get_current_user)):
    if user.role != UserRole.superadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Superadmin required")
    return user

def _require_self_or_admin(user_id: int, current: User = Depends(get_current_user)):
    if current.role == UserRole.superadmin or current.id == user_id:
        return current
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

@router.post("/", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(_require_superadmin),
):
    notif = Notification(**payload.dict())
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

@router.get("/user/{user_id}", response_model=list[NotificationOut])
def list_user_notifications(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(_require_self_or_admin),
):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()

@router.patch("/{notif_id}/read", response_model=NotificationOut)
def mark_as_read(
    notif_id: int,
    payload: NotificationReadUpdate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    # Only recipient or superadmin can modify
    if current.role != UserRole.superadmin and notif.user_id != current.id:
        raise HTTPException(status_code=403, detail="Access denied")
    notif.is_read = payload.is_read
    db.commit()
    db.refresh(notif)
    return notif

@router.delete("/{notif_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notif_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(_require_superadmin),
):
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(notif)
    db.commit()
    return None
