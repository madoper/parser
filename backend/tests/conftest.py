"""Pytest configuration and fixtures."""
# SEMANTIC: Shared test fixtures and configuration
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from httpx import AsyncClient

from src.main import app
from src.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """SEMANTIC: Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """SEMANTIC: HTTP client for testing API endpoints."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_sitemap_xml() -> str:
    """SEMANTIC: Sample sitemap XML for testing."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/page1</loc>
            <lastmod>2024-01-01</lastmod>
            <changefreq>daily</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>https://example.com/page2</loc>
            <lastmod>2024-01-02</lastmod>
        </url>
    </urlset>'''


@pytest.fixture
def sample_sitemap_index_xml() -> str:
    """SEMANTIC: Sample sitemap index XML for testing."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <sitemap>
            <loc>https://example.com/sitemap1.xml</loc>
        </sitemap>
        <sitemap>
            <loc>https://example.com/sitemap2.xml</loc>
        </sitemap>
    </sitemapindex>'''


@pytest.fixture
def sample_html() -> str:
    """SEMANTIC: Sample HTML for testing."""
    return '''<!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <meta name="description" content="Test description">
    </head>
    <body>
        <a href="/page1">Page 1</a>
        <a href="https://example.com/page2">Page 2</a>
        <a href="#anchor">Anchor</a>
        <a href="javascript:void(0)">JavaScript</a>
    </body>
    </html>'''
