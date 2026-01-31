from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import math
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate


def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    """
    Calculate the distance between two points using the Haversine formula.
    Returns distance in km (rounded to nearest integer).
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance)


class VendorService:
    
    @staticmethod
    def get_by_id(db: Session, vendor_id: int) -> Optional[Vendor]:
        """Get vendor by ID."""
        return db.query(Vendor).filter(Vendor.id == vendor_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Vendor]:
        """Get vendor by exact name."""
        return db.query(Vendor).filter(Vendor.name == name).first()
    
    @staticmethod
    def search_by_name(db: Session, name: str, user_lat: Optional[float] = None, user_lng: Optional[float] = None) -> List[Dict[str, Any]]:
        """Search vendors by name (case-insensitive partial match) with optional distance."""
        vendors = db.query(Vendor).filter(Vendor.name.ilike(f"%{name}%")).all()
        return VendorService._add_distance_to_vendors(vendors, user_lat, user_lng)
    
    @staticmethod
    def get_all(db: Session, user_lat: Optional[float] = None, user_lng: Optional[float] = None) -> List[Dict[str, Any]]:
        """Get all vendors with optional distance from user location."""
        vendors = db.query(Vendor).all()
        return VendorService._add_distance_to_vendors(vendors, user_lat, user_lng)
    
    @staticmethod
    def _add_distance_to_vendors(vendors: List[Vendor], user_lat: Optional[float], user_lng: Optional[float]) -> List[Dict[str, Any]]:
        """Add distance_km to each vendor if user location is provided."""
        result = []
        for vendor in vendors:
            vendor_dict = {
                "id": vendor.id,
                "name": vendor.name,
                "image_url": vendor.image_url,
                "latitude": vendor.latitude,
                "longitude": vendor.longitude,
                "email": vendor.email,
                "phone_number": vendor.phone_number,
                "created_at": vendor.created_at,
                "updated_at": vendor.updated_at,
                "distance_km": None
            }
            if user_lat is not None and user_lng is not None:
                vendor_dict["distance_km"] = calculate_distance_km(
                    user_lat, user_lng, vendor.latitude, vendor.longitude
                )
            result.append(vendor_dict)
        
        # Sort by distance if distance is calculated
        if user_lat is not None and user_lng is not None:
            result.sort(key=lambda x: x["distance_km"])
        
        return result
    
    @staticmethod
    def create(db: Session, vendor_data: VendorCreate) -> Vendor:
        """Create a new vendor."""
        db_vendor = Vendor(
            name=vendor_data.name,
            image_url=vendor_data.image_url,
            latitude=vendor_data.latitude,
            longitude=vendor_data.longitude,
            email=vendor_data.email,
            phone_number=vendor_data.phone_number
        )
        db.add(db_vendor)
        db.commit()
        db.refresh(db_vendor)
        return db_vendor
    
    @staticmethod
    def update(db: Session, vendor_id: int, vendor_data: VendorUpdate) -> Optional[Vendor]:
        """Update an existing vendor."""
        db_vendor = VendorService.get_by_id(db, vendor_id)
        if not db_vendor:
            return None
        
        update_data = vendor_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_vendor, field, value)
        
        db.commit()
        db.refresh(db_vendor)
        return db_vendor
    
    @staticmethod
    def delete(db: Session, vendor_id: int) -> bool:
        """Delete a vendor."""
        db_vendor = VendorService.get_by_id(db, vendor_id)
        if not db_vendor:
            return False
        
        db.delete(db_vendor)
        db.commit()
        return True
    
    @staticmethod
    def search_by_location(
        db: Session, 
        lat: float, 
        lng: float, 
        radius_km: float = 10.0,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search vendors within a radius from a given location.
        Uses a simple bounding box approach for filtering.
        Returns vendors with distance_km.
        """
        # Approximate degree changes for the radius
        # 1 degree latitude ≈ 111 km
        # 1 degree longitude ≈ 111 km * cos(latitude)
        lat_range = radius_km / 111.0
        lng_range = radius_km / (111.0 * math.cos(math.radians(lat)))
        
        vendors = db.query(Vendor).filter(
            Vendor.latitude.between(lat - lat_range, lat + lat_range),
            Vendor.longitude.between(lng - lng_range, lng + lng_range)
        ).offset(skip).limit(limit).all()
        
        return VendorService._add_distance_to_vendors(vendors, lat, lng)
