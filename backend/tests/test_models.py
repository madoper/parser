"""Tests for Pydantic models."""
# SEMANTIC: Test data models validation
import pytest
from pydantic import ValidationError
from datetime import datetime

from src.models.parsing import (
    SitemapRequest,
    SitemapResponse,
    ParsedURL,
    ParsingTask,
    TaskStatus,
)


class TestModels:
    """SEMANTIC: Test suite for Pydantic models."""

    def test_sitemap_request_valid(self):
        """SEMANTIC: Test valid SitemapRequest."""
        request = SitemapRequest(
            url="https://example.com/sitemap.xml",
            max_depth=3,
            follow_nested=True
        )
        assert request.url == "https://example.com/sitemap.xml"
        assert request.max_depth == 3
        assert request.follow_nested is True

    def test_sitemap_request_invalid_url(self):
        """SEMANTIC: Test invalid URL validation."""
        with pytest.raises(ValidationError):
            SitemapRequest(
                url="not-a-url",
                max_depth=3
            )

    def test_sitemap_request_max_depth_bounds(self):
        """SEMANTIC: Test max_depth bounds validation."""
        # Should fail for values outside 1-10 range
        with pytest.raises(ValidationError):
            SitemapRequest(
                url="https://example.com/sitemap.xml",
                max_depth=0
            )
        
        with pytest.raises(ValidationError):
            SitemapRequest(
                url="https://example.com/sitemap.xml",
                max_depth=11
            )

    def test_sitemap_response_valid(self):
        """SEMANTIC: Test valid SitemapResponse."""
        response = SitemapResponse(
            task_id="test-123",
            status=TaskStatus.COMPLETED,
            total_urls=10,
            urls=["https://example.com/page1"]
        )
        assert response.task_id == "test-123"
        assert response.status == TaskStatus.COMPLETED
        assert response.total_urls == 10

    def test_parsed_url_valid(self):
        """SEMANTIC: Test valid ParsedURL."""
        url = ParsedURL(
            url="https://example.com/page",
            lastmod=datetime.utcnow(),
            changefreq="daily",
            priority=0.8
        )
        assert url.url == "https://example.com/page"
        assert url.priority == 0.8

    def test_parsed_url_priority_bounds(self):
        """SEMANTIC: Test priority bounds validation."""
        with pytest.raises(ValidationError):
            ParsedURL(
                url="https://example.com/page",
                priority=1.5  # Exceeds max
            )

    def test_parsing_task_valid(self):
        """SEMANTIC: Test valid ParsingTask."""
        task = ParsingTask(
            id="task-123",
            url="https://example.com/sitemap.xml",
            status=TaskStatus.PENDING,
            config={"max_depth": 3, "follow_nested": True},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        assert task.id == "task-123"
        assert task.status == TaskStatus.PENDING

    def test_parsing_task_config_validation(self):
        """SEMANTIC: Test config validation."""
        with pytest.raises(ValidationError):
            ParsingTask(
                id="task-123",
                url="https://example.com/sitemap.xml",
                status=TaskStatus.PENDING,
                config={"invalid": "config"},  # Missing required keys
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

    def test_task_status_enum(self):
        """SEMANTIC: Test TaskStatus enum values."""
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.RUNNING == "running"
        assert TaskStatus.COMPLETED == "completed"
        assert TaskStatus.FAILED == "failed"
        assert TaskStatus.CANCELLED == "cancelled"
