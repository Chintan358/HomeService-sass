from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # the provider this tech works for
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)

    # relationships
    user = relationship("User", foreign_keys=[user_id])
    provider = relationship("User", foreign_keys=[provider_id])

    def __repr__(self) -> str:
        return f"<Technician {self.name} (User {self.user_id})>"
