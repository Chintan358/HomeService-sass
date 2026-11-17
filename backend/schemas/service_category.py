"""Pydantic schemas for Service Category API.
"""

from pydantic import BaseModel, Field
from typing import Optional

class ServiceCategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True

class ServiceCategoryCreate(ServiceCategoryBase):
    pass

class ServiceCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceCategoryOut(ServiceCategoryBase):
    id: int

    class Config:
        orm_mode = True
