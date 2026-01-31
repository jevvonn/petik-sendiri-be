import os
import joblib
import httpx
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.plant import Plant

router = APIRouter()

# Load model and label encoder
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "model-ai", "crop-recommendation")
MODEL_PATH = os.path.join(MODEL_DIR, "crop_recommendation_model.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "crop_recommendation_label_encoder.pkl")

# Load the model and label encoder at startup
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)


class PlantRecommendationRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of the location")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of the location")
    num_recommendations: int = Field(default=3, ge=1, le=10, description="Number of plant recommendations to return")


class PlantRecommendation(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    category: str
    difficulty_level: Optional[str] = None
    duration_days: Optional[str] = None
    image_url: Optional[str] = None
    probability: float
    
    class Config:
        from_attributes = True


class WeatherData(BaseModel):
    temperature: float
    humidity: float
    rainfall: float


class PlantRecommendationResponse(BaseModel):
    weather_data: WeatherData
    recommendations: List[PlantRecommendation]


async def get_weather_data(latitude: float, longitude: float) -> dict:
    """
    Fetch weather data from Open-Meteo API.
    Returns average temperature (Celsius), humidity (%), and rainfall (mm) for the past 30 days.
    Uses historical data to provide stable recommendations that don't change throughout the day.
    """
    # Calculate date range for the past 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Format dates as YYYY-MM-DD
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    # Open-Meteo Historical API - get hourly data for the past 30 days
    # We'll get data at specific hours (6:00, 12:00, 18:00) to average
    meteo_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date_str}&end_date={end_date_str}"
        f"&hourly=temperature_2m,relative_humidity_2m"
        f"&daily=precipitation_sum"
        f"&timezone=auto"
    )
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(meteo_url)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to fetch weather data from Open-Meteo: {response.text}"
            )
        
        meteo_data = response.json()
        
        # Extract hourly data
        hourly_data = meteo_data.get("hourly", {})
        hourly_times = hourly_data.get("time", [])
        hourly_temps = hourly_data.get("temperature_2m", [])
        hourly_humidity = hourly_data.get("relative_humidity_2m", [])
        
        # Filter data for specific hours (6:00, 12:00, 18:00) to get representative daily values
        # These hours capture morning, midday, and evening conditions
        target_hours = [6, 12, 18]
        filtered_temps = []
        filtered_humidity = []
        
        for i, time_str in enumerate(hourly_times):
            # Parse hour from time string (format: "2024-01-15T06:00")
            hour = int(time_str.split("T")[1].split(":")[0])
            if hour in target_hours:
                if hourly_temps[i] is not None:
                    filtered_temps.append(hourly_temps[i])
                if hourly_humidity[i] is not None:
                    filtered_humidity.append(hourly_humidity[i])
        
        # Calculate averages
        avg_temperature = sum(filtered_temps) / len(filtered_temps) if filtered_temps else 25.0
        avg_humidity = sum(filtered_humidity) / len(filtered_humidity) if filtered_humidity else 70.0
        
        # Sum up the 30-day precipitation
        rainfall = 0.0
        if "daily" in meteo_data and "precipitation_sum" in meteo_data["daily"]:
            precipitation_values = meteo_data["daily"]["precipitation_sum"]
            rainfall = sum(p for p in precipitation_values if p is not None)
        
        return {
            "temperature": round(avg_temperature, 2),
            "humidity": round(avg_humidity, 2),
            "rainfall": round(rainfall, 2)
        }


def predict_top_k(temp: float, humidity: float, rainfall: float, k: int = 3) -> List[tuple]:
    """
    Predict top k plant recommendations based on weather parameters.
    """
    input_df = pd.DataFrame([{
        "temp": temp,
        "humidity": humidity,
        "rainfall": rainfall
    }])

    probs = model.predict_proba(input_df)[0]
    top_idx = np.argsort(probs)[-k:][::-1]

    return list(zip(
        label_encoder.inverse_transform(top_idx),
        probs[top_idx]
    ))


@router.post(
    "/plant-recommendation",
    response_model=PlantRecommendationResponse,
    summary="Get Plant Recommendations",
    description="Get plant recommendations based on location weather data"
)
async def get_plant_recommendation(
    request: PlantRecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Get plant recommendations based on weather conditions at the specified location.
    
    - **latitude**: Latitude of the location (-90 to 90)
    - **longitude**: Longitude of the location (-180 to 180)
    - **num_recommendations**: Number of recommendations to return (1-10, default: 3)
    
    The endpoint fetches historical weather data (30-day average temperature, humidity, 
    and total rainfall) from Open-Meteo API and uses a machine learning model to recommend 
    suitable plants. Using historical averages ensures stable recommendations throughout the day.
    """
    # Get weather data from Open-Meteo
    weather = await get_weather_data(request.latitude, request.longitude)
    
    # Request more recommendations from ML model than needed to account for 
    # plants that may not exist in database. Then filter to requested amount.
    buffer_multiplier = 3  # Get 3x more recommendations to ensure we have enough matches
    ml_recommendations_count = min(request.num_recommendations * buffer_multiplier, 21)  # Max 21 (all classes)
    
    # Get plant recommendations from ML model
    recommendations = predict_top_k(
        temp=weather["temperature"],
        humidity=weather["humidity"],
        rainfall=weather["rainfall"],
        k=ml_recommendations_count
    )
    
    # Convert plant names to slugs (lowercase, spaces to hyphens)
    def to_slug(name: str) -> str:
        return name.lower().replace(" ", "-")
    
    # Extract plant names and create probability mapping with slugs
    plant_slugs = [to_slug(plant_name) for plant_name, _ in recommendations]
    prob_mapping = {to_slug(plant_name): float(prob) for plant_name, prob in recommendations}
    
    # Query database for plants matching the recommended slugs using IN query
    plants_from_db = db.query(Plant).filter(Plant.slug.in_(plant_slugs)).all()
    
    # Create a mapping of plant slug to plant object for ordering
    plant_mapping = {plant.slug: plant for plant in plants_from_db}
    
    # Build response maintaining the order from ML model (highest probability first)
    # Only include plants that exist in the database, limited to requested count
    recommendation_list = []
    for slug in plant_slugs:
        if slug in plant_mapping and len(recommendation_list) < request.num_recommendations:
            plant = plant_mapping[slug]
            recommendation_list.append(
                PlantRecommendation(
                    id=plant.id,
                    name=plant.name,
                    slug=plant.slug,
                    description=plant.description,
                    category=plant.category,
                    difficulty_level=plant.difficulty_level,
                    duration_days=plant.duration_days,
                    image_url=plant.image_url,
                    probability=prob_mapping[slug]
                )
            )
    
    return PlantRecommendationResponse(
        weather_data=WeatherData(
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            rainfall=weather["rainfall"]
        ),
        recommendations=recommendation_list
    )
