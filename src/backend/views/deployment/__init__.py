from fastapi import APIRouter

from .health import router as health_router

deployment_router = APIRouter(prefix="/deployment")
deployment_router.include_router(health_router)
