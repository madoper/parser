"""Tests for parsing service."""
# SEMANTIC: Test parsing service functionality
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.services.parsing_service import ParsingService


@pytest.mark.asyncio
class TestParsingService:
    """SEMANTIC: Test suite for ParsingService class."""

    async def test_service_initialization(self):
        """SEMANTIC: Test service initializes correctly."""
        service = ParsingService()
        assert service is not None
        assert len(service.parsed_urls) == 0
        assert len(service.tasks) == 0
        await service.close()

    async def test_create_task(self):
        """SEMANTIC: Test task creation."""
        service = ParsingService()
        
        task = service.create_task(
            url="https://example.com/sitemap.xml",
            config={"max_depth": 3, "follow_nested": True}
        )
        
        assert task["id"] is not None
        assert task["url"] == "https://example.com/sitemap.xml"
        assert task["status"] == "pending"
        assert "created_at" in task
        
        await service.close()

    async def test_get_task_status(self):
        """SEMANTIC: Test retrieving task status."""
        service = ParsingService()
        
        task = service.create_task(
            url="https://example.com/sitemap.xml",
            config={"max_depth": 3, "follow_nested": True}
        )
        
        status = service.get_task_status(task["id"])
        assert status is not None
        assert status["id"] == task["id"]
        assert status["status"] == "pending"
        
        await service.close()

    async def test_update_task_status(self):
        """SEMANTIC: Test updating task status."""
        service = ParsingService()
        
        task = service.create_task(
            url="https://example.com/sitemap.xml",
            config={"max_depth": 3, "follow_nested": True}
        )
        
        service.update_task_status(
            task["id"],
            status="completed",
            result={"total_urls": 100}
        )
        
        status = service.get_task_status(task["id"])
        assert status["status"] == "completed"
        assert status["result"]["total_urls"] == 100
        
        await service.close()

    async def test_extract_urls_from_html(self, sample_html):
        """SEMANTIC: Test extracting URLs from HTML."""
        service = ParsingService()
        
        urls = await service.extract_urls_from_html(
            sample_html,
            "https://example.com"
        )
        
        # Should extract valid URLs, skip anchors and javascript
        assert len(urls) >= 2
        assert "https://example.com/page1" in urls
        assert "https://example.com/page2" in urls
        
        await service.close()

    async def test_fetch_page_content(self):
        """SEMANTIC: Test fetching page content."""
        service = ParsingService()
        
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.text = '<html><head><title>Test</title></head><body>Content</body></html>'
        mock_response.status_code = 200
        
        with patch.object(service.client, 'get', return_value=mock_response) as mock_get:
            mock_get.return_value.raise_for_status = MagicMock()
            
            result = await service.fetch_page_content("https://example.com")
            
            assert result is not None
            assert result["title"] == "Test"
            assert result["status_code"] == 200
            assert "fetched_at" in result
        
        await service.close()

    async def test_parse_sitemap_with_mock(self):
        """SEMANTIC: Test complete sitemap parsing flow."""
        service = ParsingService()
        
        # Mock SitemapParser
        with patch('src.services.parsing_service.SitemapParser') as MockParser:
            mock_parser_instance = AsyncMock()
            mock_parser_instance.parse_sitemap_url = AsyncMock(
                return_value=["https://example.com/page1", "https://example.com/page2"]
            )
            mock_parser_instance.close = AsyncMock()
            MockParser.return_value = mock_parser_instance
            
            result = await service.parse_sitemap("https://example.com/sitemap.xml")
            
            assert result["status"] == "success"
            assert result["total_urls"] == 2
            assert len(result["urls"]) == 2
        
        await service.close()
