"""Celery application configuration for async task processing."""
# SEMANTIC: Configure Celery worker and beat scheduler
from celery import Celery
from celery.schedules import crontab
import logging

from src.core.config import settings

# SEMANTIC: Configure logging
logger = logging.getLogger(__name__)

# SEMANTIC: Initialize Celery app with Redis broker
celery_app = Celery(
    "parser",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# SEMANTIC: Celery configuration
celery_app.conf.update(
    # SEMANTIC: Task execution settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # SEMANTIC: Task result settings
    result_expires=3600,  # Results expire after 1 hour
    result_persistent=True,
    
    # SEMANTIC: Task tracking
    task_track_started=settings.CELERY_TASK_TRACK_STARTED,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    task_soft_time_limit=settings.CELERY_TASK_TIME_LIMIT - 30,
    
    # SEMANTIC: Worker settings
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    
    # SEMANTIC: Task routes
    task_routes={
        "src.tasks.parsing.*": {"queue": "parsing"},
        "src.tasks.storage.*": {"queue": "storage"},
    },
    
    # SEMANTIC: Task priority
    task_default_priority=5,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# SEMANTIC: Periodic task schedule
celery_app.conf.beat_schedule = {
    # SEMANTIC: Clean up old parsing results every day at 2 AM
    "cleanup-old-results": {
        "task": "src.tasks.maintenance.cleanup_old_results",
        "schedule": crontab(hour=2, minute=0),
        "options": {"queue": "maintenance"},
    },
    # SEMANTIC: Update sitemap cache every 6 hours
    "refresh-sitemap-cache": {
        "task": "src.tasks.parsing.refresh_sitemap_cache",
        "schedule": crontab(minute=0, hour="*/6"),
        "options": {"queue": "parsing"},
    },
}

# SEMANTIC: Auto-discover tasks from modules
celery_app.autodiscover_tasks(["src.tasks"])


@celery_app.task(bind=True, name="src.tasks.debug_task")
def debug_task(self):
    """SEMANTIC: Debug task for testing Celery configuration."""
    logger.info(f"Request: {self.request!r}")
    return {"status": "ok", "task_id": self.request.id}


if __name__ == "__main__":
    celery_app.start()
