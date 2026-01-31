from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime
from decimal import Decimal


class PlantBase(BaseModel):
    slug: str
    name: str
    description: Optional[str] = None
    category: str
    difficulty_level: Optional[str] = None
    duration_days: Optional[str] = None
    recommendations: Optional[Any] = None
    prohibitions: Optional[Any] = None
    image_url: Optional[str] = None
    requirements: Any
    unit: Optional[str] = None
    market_price_per_unit: Optional[Decimal] = None
    growth_phases: Optional[Any] = None
    common_diseases: Optional[Any] = None


class PlantResponse(PlantBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PlantListResponse(BaseModel):
    id: int
    slug: str
    name: str
    description: Optional[str] = None
    category: str
    difficulty_level: Optional[str] = None
    duration_days: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True
