from pydantic import BaseModel
from typing import List, Optional


class PredictionItem(BaseModel):
    disease: str
    confidence: float


class PlantDiseaseResponse(BaseModel):
    plant_type: Optional[str] = None
    disease_name: Optional[str] = None
    confidence: float
    is_healthy: Optional[bool] = None
    description: Optional[str] = None
    treatment: Optional[str] = None
    prevention: Optional[str] = None
    all_predictions: List[PredictionItem]
    plant_match: bool
    warning: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "plant_type": "Tomat",
                "disease_name": "Hawar Daun Awal",
                "confidence": 0.95,
                "is_healthy": False,
                "description": "Penyakit jamur Alternaria solani dengan bercak coklat target pada daun bawah.",
                "treatment": "Aplikasi fungisida chlorothalonil atau mancozeb setiap 7-10 hari. Pemangkasan daun terinfeksi.",
                "prevention": "Mulsa plastik, drip irrigation, jaga jarak tanam, rotasi tanaman minimal 2 tahun.",
                "all_predictions": [
                    {"disease": "Tomato_Early_blight", "confidence": 0.95},
                    {"disease": "Tomato_Late_blight", "confidence": 0.03},
                    {"disease": "Tomato_healthy", "confidence": 0.02}
                ],
                "plant_match": True,
                "warning": None
            }
        }
