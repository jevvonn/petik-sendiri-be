from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base


class Plant(Base):
    __tablename__ = "plants"
    
    id = Column(BigInteger, primary_key=True, index=True)
    slug = Column(String(100), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)
    difficulty_level = Column(String(255), nullable=True)
    duration_days = Column(String(255), nullable=True)
    recommendations = Column(JSONB, nullable=True)
    prohibitions = Column(JSONB, nullable=True)
    image_url = Column(String(500), nullable=True)
    requirements = Column(JSONB, nullable=False)
    unit = Column(String(50), nullable=True)
    market_price_per_unit = Column(DECIMAL(precision=12, scale=2), nullable=True)
    growth_phases = Column(JSONB, nullable=True)
    common_diseases = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Plant(id={self.id}, name={self.name}, category={self.category})>"
