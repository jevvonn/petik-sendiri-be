from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, plant_recommendation

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(plant_recommendation.router, prefix="/recommendation", tags=["Recommendation"])
