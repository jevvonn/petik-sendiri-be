from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.models.plant import Plant
from app.schemas.plant import PlantResponse, PlantListResponse

router = APIRouter()


@router.get("", response_model=List[PlantListResponse])
async def get_all_plants(db: Session = Depends(get_db)):
    """
    Get all plants.
    """
    plants = db.query(Plant).order_by(Plant.name).all()
    return plants


@router.get("/{plant_name}", response_model=PlantResponse)
async def get_plant_by_name(
    plant_name: str,
    db: Session = Depends(get_db)
):
    """
    Get plant details by slug/name.
    The plant_name parameter should be the slug of the plant (e.g., 'bawang-putih').
    """
    plant = db.query(Plant).filter(Plant.slug == plant_name).first()
    
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    # Convert JSONB fields to proper Python objects for JSON response
    plant_data = {
        "id": plant.id,
        "slug": plant.slug,
        "name": plant.name,
        "description": plant.description,
        "category": plant.category,
        "difficulty_level": plant.difficulty_level,
        "duration_days": plant.duration_days,
        "recommendations": plant.recommendations,
        "prohibitions": plant.prohibitions,
        "image_url": plant.image_url,
        "requirements": plant.requirements,
        "unit": plant.unit,
        "market_price_per_unit": plant.market_price_per_unit,
        "growth_phases": plant.growth_phases,
        "common_diseases": plant.common_diseases,
        "created_at": plant.created_at
    }
    
    return PlantResponse(**plant_data)
