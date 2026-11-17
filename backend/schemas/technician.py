"""Pydantic schemas for Technician management.
"""

from pydantic import BaseModel, Field
from typing import Optional

class TechnicianBase(BaseModel):
    name: str = Field(..., max_length=100)
    phone: Optional[str] = None
    is_active: Optional[bool] = True

class TechnicianCreate(TechnicianBase):
    user_id: int = Field(..., description="User ID linked to this technician")
    provider_id: Optional[int] = Field(None, description="Provider ID this technician works for")

class TechnicianUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    provider_id: Optional[int] = None

class TechnicianOut(TechnicianBase):
    id: int
    user_id: int
    provider_id: Optional[int]

    class Config:
        orm_mode = True
