from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate


class VendorService:
    
    @staticmethod
    def get_by_id(db: Session, vendor_id: int) -> Optional[Vendor]:
        """Get vendor by ID."""
        return db.query(Vendor).filter(Vendor.id == vendor_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Vendor]:
        """Get vendor by name."""
        return db.query(Vendor).filter(Vendor.name == name).first()
    
    @staticmethod
    def get_all(db: Session) -> List[Vendor]:
        """Get all vendors."""
        return db.query(Vendor).all()
    
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
    ) -> List[Vendor]:
        """
        Search vendors within a radius from a given location.
        Uses a simple bounding box approach for filtering.
        """
        # Approximate degree changes for the radius
        # 1 degree latitude ≈ 111 km
        # 1 degree longitude ≈ 111 km * cos(latitude)
        import math
        lat_range = radius_km / 111.0
        lng_range = radius_km / (111.0 * math.cos(math.radians(lat)))
        
        return db.query(Vendor).filter(
            Vendor.latitude.between(lat - lat_range, lat + lat_range),
            Vendor.longitude.between(lng - lng_range, lng + lng_range)
        ).offset(skip).limit(limit).all()
