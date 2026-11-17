from sqlalchemy import Column, Integer, String, Boolean, Text
from ..core.database import Base

class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<ServiceCategory {self.name}>"
