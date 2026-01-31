from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from app.schemas.plant_disease import PlantDiseaseResponse
from app.services.plant_disease_service import get_plant_disease_predictor

router = APIRouter()


@router.post("/predict", response_model=PlantDiseaseResponse)
async def predict_plant_disease(
    image: UploadFile = File(..., description="Image of plant leaf to analyze for disease"),
    plant_type: Optional[str] = Form(None, description="Optional: Type of plant (e.g., 'tomat', 'kentang', 'paprika') for validation")
):
    """
    Predict plant disease from an uploaded image.
    
    Upload an image of a plant leaf and the AI model will analyze it to detect
    any diseases. The model can identify diseases in:
    - Paprika (Bell Pepper)
    - Kentang (Potato)
    - Tomat (Tomato)
    
    Optionally provide `plant_type` to validate if the detected plant matches your input.
    
    Returns:
    - plant_type: Detected plant type (in Indonesian)
    - disease_name: Name of the disease (in Indonesian)
    - confidence: Prediction confidence score
    - is_healthy: Whether the plant is healthy
    - description: Description of the disease
    - treatment: Recommended treatment
    - prevention: Prevention tips
    - all_predictions: Top 3 predictions with confidence scores
    - plant_match: Whether detected plant matches user input (if provided)
    - warning: Warning message if plant type doesn't match
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Read image bytes
    try:
        image_bytes = await image.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read image file: {str(e)}"
        )
    
    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if len(image_bytes) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum allowed size is 10MB"
        )
    
    # Get predictor and make prediction
    try:
        predictor = get_plant_disease_predictor()
        result = predictor.predict(image_bytes, plant_type)
        return result
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
