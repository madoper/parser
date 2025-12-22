"""Sitemap parsing API endpoints."""
# SEMANTIC: API router for sitemap parsing operations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from celery.result import AsyncResult

from src.tasks import parse_sitemap_task
from src.celery_app import celery_app

# SEMANTIC: Initialize router for sitemap endpoints
router = APIRouter(prefix="/sitemap", tags=["sitemap"])


# SEMANTIC: Request model for sitemap URL submission
class SitemapRequest(BaseModel):
    """Request model for sitemap parsing."""
    url: HttpUrl
    max_depth: Optional[int] = 3
    follow_nested: Optional[bool] = True


# SEMANTIC: Response model for parsing tasks
class SitemapResponse(BaseModel):
    """Response model for sitemap parsing."""
    task_id: str
    status: str
    total_urls: int = 0
    urls: Optional[List[str]] = []


@router.post("/parse", response_model=SitemapResponse)
async def parse_sitemap(request: SitemapRequest):
    """Parse sitemap and extract all URLs from sitemap index."""
    # SEMANTIC: Handle sitemap parsing via service
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Received request to parse sitemap")
    logger.info(f"Request data: {request}")
    try:
        task = parse_sitemap_task.delay(str(request.url), request.max_depth or 3, request.follow_nested or True)
        logger.info(f"Started Celery task: {task.id}")
        return SitemapResponse(
            task_id=task.id,
            status="pending",
            total_urls=0,
            urls=[]
        )
    except Exception as e:
        logger.error(f"Error starting parse task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get parsing task status and results."""
    # SEMANTIC: Retrieve task status from Celery result backend
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        response = {
            "task_id": task_id,
            "status": "pending",
            "total_urls": 0,
            "urls": []
        }
    elif result.state == "PROGRESS":
        response = {
            "task_id": task_id,
            "status": "progress",
            "total_urls": result.info.get("total_urls", 0),
            "urls": result.info.get("urls", [])
        }
    elif result.state == "SUCCESS":
        response = {
            "task_id": task_id,
            "status": "completed",
            "total_urls": len(result.result.get("urls", [])),
            "urls": result.result.get("urls", [])
        }
    else:
        response = {
            "task_id": task_id,
            "status": "failed",
            "error": str(result.info),
            "total_urls": 0,
            "urls": []
        }
    return response
