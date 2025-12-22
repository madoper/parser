"""Tests for API endpoints."""
# SEMANTIC: Test FastAPI endpoints
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
class TestAPIEndpoints:
    """SEMANTIC: Test suite for API endpoints."""

    async def test_health_check(self, client: AsyncClient):
        """SEMANTIC: Test health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    async def test_ready_check(self, client: AsyncClient):
        """SEMANTIC: Test readiness check endpoint."""
        response = await client.get("/ready")
        assert response.status_code in [200, 503]
        data = response.json()
        assert "ready" in data

    async def test_parse_sitemap_endpoint(self, client: AsyncClient):
        """SEMANTIC: Test sitemap parsing endpoint."""
        # Mock the parsing service
        with patch('src.api.v1.sitemap.ParsingService') as MockService:
            mock_service = AsyncMock()
            MockService.return_value = mock_service
            
            payload = {
                "url": "https://example.com/sitemap.xml",
                "max_depth": 3,
                "follow_nested": True
            }
            
            response = await client.post("/api/v1/sitemap/parse", json=payload)
            
            # Should return task info
            assert response.status_code in [200, 201]
            data = response.json()
            assert "task_id" in data
            assert "status" in data

    async def test_invalid_url_validation(self, client: AsyncClient):
        """SEMANTIC: Test URL validation."""
        payload = {
            "url": "not-a-valid-url",
            "max_depth": 3
        }
        
        response = await client.post("/api/v1/sitemap/parse", json=payload)
        assert response.status_code == 422  # Validation error

    async def test_max_depth_validation(self, client: AsyncClient):
        """SEMANTIC: Test max_depth parameter validation."""
        payload = {
            "url": "https://example.com/sitemap.xml",
            "max_depth": 20  # Exceeds limit
        }
        
        response = await client.post("/api/v1/sitemap/parse", json=payload)
        assert response.status_code == 422  # Validation error
