from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..core.database import get_db
from ..models.booking import Booking, BookingStatus
from ..models.user import User, UserRole
from ..schemas.booking import BookingCreate, BookingOut, BookingStatusUpdate
from ..utils.dependencies import get_current_user

router = APIRouter()

def _require_customer(user: User = Depends(get_current_user)):
    if user.role != UserRole.customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customers can create bookings")
    return user

def _require_provider(user: User = Depends(get_current_user)):
    if user.role != UserRole.provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only providers can modify booking status")
    return user

def _require_superadmin(user: User = Depends(get_current_user)):
    if user.role != UserRole.superadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Superadmin required")
    return user

@router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    customer: User = Depends(_require_customer),
):
    # Prevent double‑booking for the same provider overlapping the requested time window
    overlapping = (
        db.query(Booking)
        .filter(
            Booking.provider_id == payload.provider_id,
            Booking.status.in_([
                BookingStatus.pending,
                BookingStatus.confirmed,
                BookingStatus.provider_assigned,
                BookingStatus.in_progress,
            ]),
            Booking.start_time < payload.end_time,
            Booking.end_time > payload.start_time,
        )
        .first()
    )
    if overlapping:
        raise HTTPException(status_code=400, detail="Provider already has a booking in the requested time slot")

    booking = Booking(
        customer_id=customer.id,
        provider_id=payload.provider_id,
        service_id=payload.service_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        address=payload.address,
        description=payload.description,
        status=BookingStatus.pending,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    # Customers can see their own, providers can see theirs, superadmin can see any
    if user.role == UserRole.customer and booking.customer_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if user.role == UserRole.provider and booking.provider_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return booking

@router.get("/", response_model=list[BookingOut])
def list_bookings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role == UserRole.superadmin:
        return db.query(Booking).all()
    if user.role == UserRole.customer:
        return db.query(Booking).filter(Booking.customer_id == user.id).all()
    if user.role == UserRole.provider:
        return db.query(Booking).filter(Booking.provider_id == user.id).all()
    raise HTTPException(status_code=403, detail="Unsupported role")

@router.put("/{booking_id}/status", response_model=BookingOut)
def update_status(
    booking_id: int,
    payload: BookingStatusUpdate,
    db: Session = Depends(get_db),
    provider: User = Depends(_require_provider),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.provider_id != provider.id:
        raise HTTPException(status_code=403, detail="Provider can only modify its own bookings")
    booking.status = payload.status
    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    # Only the customer who created it (or superadmin) may cancel
    if user.role == UserRole.customer and booking.customer_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot cancel others' bookings")
    if user.role == UserRole.superadmin:
        pass
    # Update status to cancelled
    booking.status = BookingStatus.cancelled
    db.commit()
    return None
