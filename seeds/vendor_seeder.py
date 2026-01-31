"""
Vendor Seeder - Seeds vendor data into the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.vendor import Vendor


def seed_vendors():
    """Create vendor data if not exists."""
    db: Session = SessionLocal()
    
    try:
        # Check if vendors already exist
        existing_vendors = db.query(Vendor).count()
        
        if existing_vendors > 0:
            print(f"Vendors already exist ({existing_vendors} vendors). Skipping...")
            return
        
        vendors_data = [
            {
                "name": "Paritama Landscape",
                "phone_number": "082137727376",
                "email": "paritamalandscape@gmail.com",
                "latitude": -6.9932,
                "longitude": 110.4201,
                "image_url": "/vendor/vendor.jpg"
            },
            {
                "name": "Salaam Garden",
                "phone_number": "085950768879",
                "email": "Info@salaamgarden.com",
                "latitude": -7.0515,
                "longitude": 110.4389,
                "image_url": "/vendor/vendor.jpg"
            },
            {
                "name": "Garden Center",
                "phone_number": "081334518899",
                "email": "admin@gardencenter.co.id",
                "latitude": -6.988,
                "longitude": 110.3654,
                "image_url": "/vendor/vendor.jpg"
            },
            {
                "name": "CV Plantamor",
                "phone_number": "0247616800",
                "email": "plantamor@yahoo.com",
                "latitude": -7.0021,
                "longitude": 110.4755,
                "image_url": "/vendor/vendor.jpg"
            },
            {
                "name": "Bunga Garden SAGARA",
                "phone_number": "085607448745",
                "email": None,  # No email provided
                "latitude": -6.9699,
                "longitude": 110.415,
                "image_url": "/vendor/vendor.jpg"
            }
        ]
        
        # Create vendor objects
        for vendor_data in vendors_data:
            vendor = Vendor(**vendor_data)
            db.add(vendor)
        
        db.commit()
        print(f"✅ Successfully seeded {len(vendors_data)} vendors!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding vendors: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_vendors()
