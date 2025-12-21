"""API v1 routers initialization."""
# SEMANTIC: Router configuration for API v1 endpoints
from fastapi import APIRouter

# SEMANTIC: Initialize main API router for v1 endpoints
router = APIRouter(prefix="/api/v1", tags=["v1"])

# SEMANTIC: Import routers for specific API endpoints
# from .sitemap import router as sitemap_router
# router.include_router(sitemap_router)

__all__ = ["router"]
