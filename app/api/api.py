from fastapi import APIRouter
from app.api import endpoints
from app.api.dashboard import router as dashboard_router

api_router = APIRouter()
api_router.include_router(endpoints.router, tags=["ecommerce"])
api_router.include_router(dashboard_router, tags=["dashboard"])
