"""Analytics response schemas.
Provides summary data for admin, provider, and customer dashboards.
"""

from pydantic import BaseModel
from typing import List, Optional

class AdminDashboard(BaseModel):
    total_customers: int
    total_providers: int
    total_technicians: int
    total_bookings: int
    pending_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_revenue: float
    platform_commission: float
    top_service_category: Optional[str] = None
    monthly_bookings: List[int]  # 12 values for each month
    monthly_revenue: List[float]

class ProviderDashboard(BaseModel):
    total_bookings: int
    todays_bookings: int
    pending_requests: int
    completed_services: int
    total_earnings: float
    average_rating: Optional[float] = None
    monthly_revenue: List[float]

class CustomerDashboard(BaseModel):
    upcoming_appointments: int
    previous_bookings: int
    pending_payments: int
    favorite_services: List[int]  # IDs of favourite service providers
    booking_status_counts: dict
