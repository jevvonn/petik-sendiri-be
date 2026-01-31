from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.services.vendor_service import VendorService
from app.api.deps import get_current_active_user, get_current_superuser
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[VendorResponse], summary="Get All Vendors")
def get_vendors(
    db: Session = Depends(get_db)
):
    """
    Retrieve all vendors.
    """
    vendors = VendorService.get_all(db)
    return vendors


@router.get("/search", response_model=List[VendorResponse], summary="Search Vendors by Location")
def search_vendors_by_location(
    latitude: float = Query(..., description="Latitude of the search center"),
    longitude: float = Query(..., description="Longitude of the search center"),
    radius_km: float = Query(10.0, description="Search radius in kilometers"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Search vendors within a radius from a given location.
    
    - **latitude**: Latitude of the search center
    - **longitude**: Longitude of the search center
    - **radius_km**: Search radius in kilometers (default: 10)
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    vendors = VendorService.search_by_location(
        db, 
        lat=latitude, 
        lng=longitude, 
        radius_km=radius_km,
        skip=skip, 
        limit=limit
    )
    return vendors


@router.get("/{vendor_id}", response_model=VendorResponse, summary="Get Vendor by ID")
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific vendor by ID.
    
    - **vendor_id**: The ID of the vendor to retrieve
    """
    vendor = VendorService.get_by_id(db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    return vendor


@router.post("/", response_model=VendorResponse, status_code=status.HTTP_201_CREATED, summary="Create Vendor")
def create_vendor(
    vendor_data: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Create a new vendor. (Admin only)
    
    - **name**: Vendor name (required)
    - **image_url**: URL to vendor image (optional)
    - **latitude**: Vendor location latitude (required)
    - **longitude**: Vendor location longitude (required)
    - **email**: Vendor email (optional)
    - **phone_number**: Vendor phone number (required)
    """
    vendor = VendorService.create(db, vendor_data=vendor_data)
    return vendor


@router.put("/{vendor_id}", response_model=VendorResponse, summary="Update Vendor")
def update_vendor(
    vendor_id: int,
    vendor_data: VendorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Update an existing vendor. (Admin only)
    
    - **vendor_id**: The ID of the vendor to update
    """
    vendor = VendorService.update(db, vendor_id=vendor_id, vendor_data=vendor_data)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    return vendor


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Vendor")
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Delete a vendor. (Admin only)
    
    - **vendor_id**: The ID of the vendor to delete
    """
    success = VendorService.delete(db, vendor_id=vendor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    return None
