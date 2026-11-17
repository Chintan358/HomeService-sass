"""Pydantic schemas for the Booking API.
These reflect the Booking model defined in ``backend/models/booking.py``.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    provider_assigned = "provider_assigned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    rejected = "rejected"

class BookingBase(BaseModel):
    service_id: int = Field(..., description="ID of the service being booked")
    start_time: datetime = Field(..., description="Requested start datetime")
    end_time: datetime = Field(..., description="Requested end datetime")
    address: str = Field(..., max_length=255)
    description: Optional[str] = None

class BookingCreate(BookingBase):
    provider_id: int = Field(..., description="ID of the chosen service provider")

class BookingOut(BookingBase):
    id: int
    customer_id: int
    provider_id: int
    status: BookingStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BookingStatusUpdate(BaseModel):
    status: BookingStatus
