"""Celery tasks for asynchronous processing."""
# SEMANTIC: Celery task definitions for background processing
import asyncio
import logging
from typing import Dict, Any

from src.celery_app import celery_app
from src.services.parsing_service import ParsingService

# SEMANTIC: Configure logging for tasks
logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="src.tasks.parsing.parse_sitemap")
def parse_sitemap_task(self, url: str, max_depth: int = 3, follow_nested: bool = True) -> Dict[str, Any]:
    """Parse sitemap asynchronously using Celery.

    Args:
        url: Sitemap or website URL to parse
        max_depth: Maximum depth for nested sitemap indices
        follow_nested: Whether to follow nested sitemaps

    Returns:
        Dictionary with parsing results
    """
    logger.info(f"Starting Celery task to parse sitemap: {url}")

    try:
        # SEMANTIC: Create parsing service instance
        service = ParsingService()

        # SEMANTIC: Run async parsing in event loop
        result = asyncio.run(service.parse_sitemap(url, max_depth))

        # SEMANTIC: Save results to database
        metadata = {
            "task_id": self.request.id,
            "celery_task_id": self.request.id,
            "status": result["status"],
            "error": result.get("error"),
        }
        asyncio.run(service.save_parsing_results(self.request.id, result["urls"], metadata))

        # SEMANTIC: Close service
        asyncio.run(service.close())

        logger.info(f"Completed parsing task {self.request.id} for {url}: {len(result['urls'])} URLs found")
        return result

    except Exception as e:
        logger.error(f"Error in parse_sitemap_task: {e}", exc_info=True)
        raise