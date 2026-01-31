from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


# ============ Plant for Generate ============
class PlantCategoryEnum:
    LEAFY_VEGETABLES = "leafy_vegetables"
    FRUIT_VEGETABLES = "fruit_vegetables"
    HERBS = "herbs"
    MEDICINAL_PLANTS = "medicinal_plants"


class PlantForGenerate(BaseModel):
    id: str
    name: str  # Indonesian name
    category: str
    prompt_name: str  # English name for prompt


class PlantForGenerateResponse(BaseModel):
    plants: List[PlantForGenerate]


# ============ Design Style ============
class DesignStyle(BaseModel):
    id: str
    name: str  # Indonesian name
    description: str  # Indonesian description


class DesignStyleResponse(BaseModel):
    styles: List[DesignStyle]


# ============ Generate Request/Response ============
class GenerateDesignRequest(BaseModel):
    image_base64: str
    plants: List[str]  # List of plant IDs
    style: str  # Style ID
    name: Optional[str] = None


class GenerateDesignResponse(BaseModel):
    id: int
    name: Optional[str] = None
    input_photo_url: str
    output_photo_url: str
    preferences: dict
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ History Response ============
class DesignHistoryItem(BaseModel):
    id: int
    name: Optional[str] = None
    input_photo_url: str
    design_output: Optional[str] = None
    preferences: Optional[dict] = None
    is_implemented: Optional[bool] = False
    rating: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class DesignHistoryResponse(BaseModel):
    designs: List[DesignHistoryItem]
    total: int
