from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.booking import Booking, BookingStatus
from ..models.payment import Payment, PaymentStatus
from ..models.technician import Technician
from ..schemas.analytics import AdminDashboard, ProviderDashboard, CustomerDashboard
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

def _require_customer(user: User = Depends(get_current_user)):
    if user.role != UserRole.customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer required")
    return user

@router.get("/admin", response_model=AdminDashboard)
def admin_dashboard(db: Session = Depends(get_db), _: User = Depends(_require_superadmin)):
    total_customers = db.query(User).filter(User.role == UserRole.customer).count()
    total_providers = db.query(User).filter(User.role == UserRole.provider).count()
    total_technicians = db.query(Technician).count()
    total_bookings = db.query(Booking).count()
    pending_bookings = db.query(Booking).filter(Booking.status == BookingStatus.pending).count()
    completed_bookings = db.query(Booking).filter(Booking.status == BookingStatus.completed).count()
    cancelled_bookings = db.query(Booking).filter(Booking.status == BookingStatus.cancelled).count()

    total_revenue = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.status == PaymentStatus.paid).scalar() or 0.0
    platform_commission = float(total_revenue) * 0.10  # assume 10% commission

    # Monthly bookings for current year (simplified)
    month_counts = []
    month_revs = []
    for m in range(1, 13):
        cnt = db.query(Booking).filter(extract('year', Booking.created_at) == func.extract('year', func.now()),
                              extract('month', Booking.created_at) == m).count()
        month_counts.append(cnt)
        rev = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(
            Payment.status == PaymentStatus.paid,
            extract('year', Payment.created_at) == func.extract('year', func.now()),
            extract('month', Payment.created_at) == m,
        ).scalar() or 0.0
        month_revs.append(float(rev))

    return AdminDashboard(
        total_customers=total_customers,
        total_providers=total_providers,
        total_technicians=total_technicians,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        completed_bookings=completed_bookings,
        cancelled_bookings=cancelled_bookings,
        total_revenue=float(total_revenue),
        platform_commission=platform_commission,
        top_service_category=None,
        monthly_bookings=month_counts,
        monthly_revenue=month_revs,
    )

@router.get("/provider", response_model=ProviderDashboard)
def provider_dashboard(db: Session = Depends(get_db), user: User = Depends(_require_provider)):
    total_bookings = db.query(Booking).filter(Booking.provider_id == user.id).count()
    todays_bookings = db.query(Booking).filter(
        Booking.provider_id == user.id,
        func.date(Booking.start_time) == func.current_date()
    ).count()
    pending_requests = db.query(Booking).filter(
        Booking.provider_id == user.id,
        Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed])
    ).count()
    completed_services = db.query(Booking).filter(
        Booking.provider_id == user.id,
        Booking.status == BookingStatus.completed
    ).count()
    total_earnings = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(
        Payment.status == PaymentStatus.paid,
        Booking.id == Payment.booking_id,
        Booking.provider_id == user.id
    ).scalar() or 0.0
    # Average rating placeholder (requires review model) – set None
    avg_rating = None
    # Monthly revenue for provider
    month_revs = []
    for m in range(1, 13):
        rev = db.query(func.coalesce(func.sum(Payment.amount), 0)).join(Booking, Booking.id == Payment.booking_id).filter(
            Payment.status == PaymentStatus.paid,
            Booking.provider_id == user.id,
            extract('year', Payment.created_at) == func.extract('year', func.now()),
            extract('month', Payment.created_at) == m,
        ).scalar() or 0.0
        month_revs.append(float(rev))
    return ProviderDashboard(
        total_bookings=total_bookings,
        todays_bookings=todays_bookings,
        pending_requests=pending_requests,
        completed_services=completed_services,
        total_earnings=float(total_earnings),
        average_rating=avg_rating,
        monthly_revenue=month_revs,
    )

@router.get("/customer", response_model=CustomerDashboard)
def customer_dashboard(db: Session = Depends(get_db), user: User = Depends(_require_customer)):
    upcoming_appointments = db.query(Booking).filter(
        Booking.customer_id == user.id,
        Booking.start_time > func.now()
    ).count()
    previous_bookings = db.query(Booking).filter(
        Booking.customer_id == user.id,
        Booking.end_time < func.now()
    ).count()
    pending_payments = db.query(Payment).join(Booking, Booking.id == Payment.booking_id).filter(
        Booking.customer_id == user.id,
        Payment.status == PaymentStatus.pending
    ).count()
    # Favorite services placeholder – return empty list
    favorite_services: list[int] = []
    # Booking status counts
    status_counts = {
        "pending": db.query(Booking).filter(Booking.customer_id == user.id, Booking.status == BookingStatus.pending).count(),
        "confirmed": db.query(Booking).filter(Booking.customer_id == user.id, Booking.status == BookingStatus.confirmed).count(),
        "in_progress": db.query(Booking).filter(Booking.customer_id == user.id, Booking.status == BookingStatus.in_progress).count(),
        "completed": db.query(Booking).filter(Booking.customer_id == user.id, Booking.status == BookingStatus.completed).count(),
        "cancelled": db.query(Booking).filter(Booking.customer_id == user.id, Booking.status == BookingStatus.cancelled).count(),
    }
    return CustomerDashboard(
        upcoming_appointments=upcoming_appointments,
        previous_bookings=previous_bookings,
        pending_payments=pending_payments,
        favorite_services=favorite_services,
        booking_status_counts=status_counts,
    )
