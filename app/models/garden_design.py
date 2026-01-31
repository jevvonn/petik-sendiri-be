from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base


class GardenDesign(Base):
    __tablename__ = "garden_designs"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=True)
    input_photo_url = Column(String(500), nullable=False)
    preferences = Column(JSONB, nullable=True)
    design_output = Column(JSONB, nullable=True)
    is_implemented = Column(Boolean, default=False, nullable=True)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", backref="garden_designs")
    
    # Check constraint for rating
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
    
    def __repr__(self):
        return f"<GardenDesign(id={self.id}, user_id={self.user_id}, name={self.name})>"
