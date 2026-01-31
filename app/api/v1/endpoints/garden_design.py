from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.garden_design_service import GardenDesignService
from app.schemas.garden_design import (
    PlantForGenerate,
    PlantForGenerateResponse,
    DesignStyle,
    DesignStyleResponse,
    GenerateDesignRequest,
    GenerateDesignResponse,
    DesignHistoryItem,
    DesignHistoryResponse,
)
from app.core.config import settings

router = APIRouter()


@router.get(
    "/plants-for-generate",
    response_model=PlantForGenerateResponse,
    summary="Get Plants for Garden Design Generation"
)
def get_plants_for_generate():
    """
    Get all available plants for garden design generation.
    
    Returns a list of plants with:
    - **id**: Plant identifier (English)
    - **name**: Plant name in Indonesian
    - **category**: Plant category
    - **prompt_name**: Plant name for AI prompt (English)
    """
    plants_data = GardenDesignService.get_plants_for_generate()
    plants = [PlantForGenerate(**p) for p in plants_data]
    return PlantForGenerateResponse(plants=plants)


@router.get(
    "/styles",
    response_model=DesignStyleResponse,
    summary="Get Design Styles"
)
def get_design_styles():
    """
    Get all available design styles for garden design generation.
    
    Returns a list of styles with:
    - **id**: Style identifier
    - **name**: Style name in Indonesian
    - **description**: Style description in Indonesian
    """
    styles_data = GardenDesignService.get_design_styles()
    styles = [DesignStyle(**s) for s in styles_data]
    return DesignStyleResponse(styles=styles)


@router.post(
    "/generate",
    response_model=GenerateDesignResponse,
    summary="Generate Urban Farming Wall Design"
)
async def generate_design(
    request: GenerateDesignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate an urban farming wall design using AI.
    
    **Request body:**
    - **image_base64**: Base64 encoded image of the wall
    - **plants**: List of plant IDs to include in the design
    - **style**: Design style ID
    - **name**: Optional name for the design
    
    **Returns:**
    - Generated design with input and output image URLs
    - Design is saved to the database for history tracking
    """
    # Validate plants
    valid_plant_ids = [p["id"] for p in GardenDesignService.get_plants_for_generate()]
    for plant_id in request.plants:
        if plant_id not in valid_plant_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid plant ID: {plant_id}"
            )
    
    # Validate style
    valid_style_ids = [s["id"] for s in GardenDesignService.get_design_styles()]
    if request.style not in valid_style_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid style ID: {request.style}"
        )
    
    # Check if Gemini API key is configured
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gemini API key not configured"
        )
    
    try:
        # Save input image
        input_photo_url = GardenDesignService.save_image_to_file(
            request.image_base64,
            "inputs",
            prefix=f"user_{current_user.id}"
        )
        
        # Generate design using Gemini
        output_image_base64 = await GardenDesignService.generate_image(
            request.image_base64,
            request.plants,
            request.style,
            settings.GEMINI_API_KEY
        )
        
        # Save output image
        output_photo_url = GardenDesignService.save_image_to_file(
            output_image_base64,
            "outputs",
            prefix=f"user_{current_user.id}"
        )
        
        # Prepare preferences
        preferences = {
            "plants": request.plants,
            "style": request.style
        }
        
        # Save to database
        garden_design = GardenDesignService.create_garden_design(
            db=db,
            user_id=current_user.id,
            name=request.name,
            input_photo_url=input_photo_url,
            output_photo_url=output_photo_url,
            preferences=preferences
        )
        
        return GenerateDesignResponse(
            id=garden_design.id,
            name=garden_design.name,
            input_photo_url=garden_design.input_photo_url,
            output_photo_url=garden_design.design_output,
            preferences=garden_design.preferences,
            created_at=garden_design.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate design: {str(e)}"
        )


@router.get(
    "/history",
    response_model=DesignHistoryResponse,
    summary="Get User's Design History"
)
def get_design_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the design generation history for the current logged-in user.
    
    **Query parameters:**
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (default: 20, max: 100)
    
    **Returns:**
    - List of design history items
    - Total count of designs for the user
    """
    designs, total = GardenDesignService.get_user_design_history(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    history_items = [
        DesignHistoryItem(
            id=design.id,
            name=design.name,
            input_photo_url=design.input_photo_url,
            design_output=design.design_output,
            preferences=design.preferences,
            is_implemented=design.is_implemented,
            rating=design.rating,
            created_at=design.created_at
        )
        for design in designs
    ]
    
    return DesignHistoryResponse(designs=history_items, total=total)


@router.get(
    "/history/{design_id}",
    response_model=DesignHistoryItem,
    summary="Get Design Detail"
)
def get_design_detail(
    design_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detail of a specific garden design.
    
    **Path parameters:**
    - **design_id**: The ID of the design to retrieve
    
    **Returns:**
    - Design detail if found and belongs to the user
    """
    design = GardenDesignService.get_design_by_id(
        db=db,
        design_id=design_id,
        user_id=current_user.id
    )
    
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    
    return DesignHistoryItem(
        id=design.id,
        name=design.name,
        input_photo_url=design.input_photo_url,
        design_output=design.design_output,
        preferences=design.preferences,
        is_implemented=design.is_implemented,
        rating=design.rating,
        created_at=design.created_at
    )
