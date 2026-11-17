"""Pydantic schemas for Notification management.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NotificationBase(BaseModel):
    title: str = Field(..., max_length=200)
    message: str

class NotificationCreate(NotificationBase):
    user_id: int = Field(..., description="Recipient user ID")

class NotificationOut(NotificationBase):
    id: int
    user_id: int
    is_read: bool = False
    created_at: datetime

    class Config:
        orm_mode = True

class NotificationReadUpdate(BaseModel):
    is_read: bool
