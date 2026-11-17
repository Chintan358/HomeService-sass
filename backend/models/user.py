from sqlalchemy import Column, Integer, String, Boolean, Enum
from ..core.database import Base
import enum

class UserRole(str, enum.Enum):
    superadmin = "superadmin"
    customer = "customer"
    provider = "provider"
    technician = "technician"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.customer)
    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role})>"
