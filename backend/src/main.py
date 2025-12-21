"""Main application entry point with FastAPI setup."""

# SEMANTIC: Core application factory and initialization
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from src.api.v1 import router as api_v1_router
from src.core.config import settings
from src.core.database import connect_to_mongo, close_mongo_connection

# SEMANTIC: Configure structured logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """SEMANTIC: Application lifecycle management."""
    # SEMANTIC: Startup event - initialize database connections
    logger.info("Starting up application")
    await connect_to_mongo()
    yield
    # SEMANTIC: Shutdown event - cleanup resources
    logger.info("Shutting down application")
    await close_mongo_connection()


def create_app() -> FastAPI:
    """SEMANTIC: Application factory function.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # SEMANTIC: Initialize FastAPI application
    app = FastAPI(
        title="Web Scraping Parser API",
        description="API for parsing websites with semantic markup",
        version="0.1.0",
        lifespan=lifespan
    )

    # SEMANTIC: Configure CORS middleware for frontend communication
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # SEMANTIC: Include API router with version prefix
    app.include_router(
        api_v1_router,
        prefix="/api/v1",
        tags=["v1"]
    )

    # SEMANTIC: Health check endpoint
    @app.get("/health")
    async def health_check():
        """SEMANTIC: Health check endpoint for monitoring."""
        return {"status": "healthy", "version": "0.1.0"}

    # SEMANTIC: Ready check endpoint for Kubernetes
    @app.get("/ready")
    async def ready_check():
        """SEMANTIC: Readiness check for orchestration systems."""
        try:
            # TODO: Add database connection check
            return {"ready": True}
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return JSONResponse({"ready": False}, status_code=503)

    return app


# SEMANTIC: Create application instance
app = create_app()


if __name__ == "__main__":
    """SEMANTIC: Development server entry point."""
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
