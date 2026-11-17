"""Pydantic schemas for authentication routes.
These are used both for request validation and for OpenAPI documentation.
"""

from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    superadmin = "superadmin"
    customer = "customer"
    provider = "provider"
    technician = "technician"

class RegisterIn(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    role: UserRole = Field(..., description="User role for RBAC")

class LoginIn(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")

class TokenOut(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type, always 'bearer'")
