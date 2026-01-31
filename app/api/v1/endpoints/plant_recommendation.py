import os
import joblib
import httpx
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

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
    plant_name: str
    probability: float


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
    Returns temperature (Celsius), humidity (%), and rainfall (mm) for 7-day forecast.
    """
    # Open-Meteo API - free, no API key needed
    # Get current temperature & humidity + 7-day rainfall forecast
    meteo_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m"
        f"&daily=precipitation_sum"
        f"&timezone=auto&forecast_days=7"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(meteo_url)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to fetch weather data from Open-Meteo: {response.text}"
            )
        
        meteo_data = response.json()
        
        # Extract current temperature and humidity
        temperature = meteo_data["current"]["temperature_2m"]
        humidity = meteo_data["current"]["relative_humidity_2m"]
        
        # Sum up the 7-day precipitation forecast
        rainfall = 0.0
        if "daily" in meteo_data and "precipitation_sum" in meteo_data["daily"]:
            precipitation_values = meteo_data["daily"]["precipitation_sum"]
            rainfall = sum(p for p in precipitation_values if p is not None)
        
        return {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
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
async def get_plant_recommendation(request: PlantRecommendationRequest):
    """
    Get plant recommendations based on weather conditions at the specified location.
    
    - **latitude**: Latitude of the location (-90 to 90)
    - **longitude**: Longitude of the location (-180 to 180)
    - **num_recommendations**: Number of recommendations to return (1-10, default: 3)
    
    The endpoint fetches current weather data (temperature, humidity, rainfall) from 
    OpenWeatherMap API and uses a machine learning model to recommend suitable plants.
    """
    # Get weather data from OpenWeatherMap
    weather = await get_weather_data(request.latitude, request.longitude)
    
    # Get plant recommendations
    recommendations = predict_top_k(
        temp=weather["temperature"],
        humidity=weather["humidity"],
        rainfall=weather["rainfall"],
        k=request.num_recommendations
    )
    
    # Format response
    recommendation_list = [
        PlantRecommendation(plant_name=plant_name, probability=float(prob))
        for plant_name, prob in recommendations
    ]
    
    return PlantRecommendationResponse(
        weather_data=WeatherData(
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            rainfall=weather["rainfall"]
        ),
        recommendations=recommendation_list
    )
