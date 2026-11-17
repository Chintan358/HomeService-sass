"""Pydantic schemas for Payment and Invoice APIs.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class PaymentBase(BaseModel):
    booking_id: int = Field(..., description="ID of the associated booking")
    amount: Decimal = Field(..., gt=0, description="Payment amount in platform currency")
    currency: str = Field(default="INR", max_length=10)

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    id: int
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    razorpay_order_id: Optional[str] = None

    class Config:
        orm_mode = True

class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus

class InvoiceOut(BaseModel):
    payment_id: int
    invoice_url: str = Field(..., description="Public URL to the generated PDF invoice")

    class Config:
        orm_mode = True
