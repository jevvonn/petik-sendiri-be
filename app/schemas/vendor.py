from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class VendorBase(BaseModel):
    name: str
    image_url: Optional[str] = None
    latitude: float
    longitude: float
    email: Optional[EmailStr] = None
    phone_number: str


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


class VendorResponse(VendorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class VendorWithDistanceResponse(VendorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    distance_km: Optional[int] = None  # Distance in km (rounded)
    google_maps_url: str
    
    class Config:
        from_attributes = True
