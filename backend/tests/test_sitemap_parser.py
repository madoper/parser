"""Tests for sitemap parser."""
# SEMANTIC: Test sitemap parsing functionality
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import xml.etree.ElementTree as ET

from src.core.parsing.sitemap_parser import SitemapParser


@pytest.mark.asyncio
class TestSitemapParser:
    """SEMANTIC: Test suite for SitemapParser class."""

    async def test_parser_initialization(self):
        """SEMANTIC: Test parser initializes correctly."""
        parser = SitemapParser()
        assert parser is not None
        assert len(parser.discovered_urls) == 0
        assert len(parser.processed_indices) == 0
        await parser.close()

    async def test_parse_sitemap_xml(self, sample_sitemap_xml):
        """SEMANTIC: Test parsing basic sitemap XML."""
        parser = SitemapParser()
        urls = parser.parse_sitemap_xml(sample_sitemap_xml, "https://example.com")
        
        assert len(urls) == 2
        assert "https://example.com/page1" in urls
        assert "https://example.com/page2" in urls
        await parser.close()

    async def test_extract_sitemap_locations(self, sample_sitemap_index_xml):
        """SEMANTIC: Test extracting sitemap locations from index."""
        parser = SitemapParser()
        root = ET.fromstring(sample_sitemap_index_xml)
        locations = parser._extract_sitemap_locations(root)
        
        assert len(locations) == 2
        assert "https://example.com/sitemap1.xml" in locations
        assert "https://example.com/sitemap2.xml" in locations
        await parser.close()

    async def test_handle_gzip_sitemap(self):
        """SEMANTIC: Test decompressing gzipped sitemap."""
        import gzip
        parser = SitemapParser()
        
        test_data = b"Test XML content"
        compressed = gzip.compress(test_data)
        
        decompressed = await parser.handle_gzip_sitemap(compressed)
        assert decompressed == test_data.decode('utf-8')
        await parser.close()

    async def test_parse_sitemap_url_with_mock(self, sample_sitemap_xml):
        """SEMANTIC: Test parsing sitemap from URL with mocked HTTP."""
        parser = SitemapParser()
        
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.text = sample_sitemap_xml
        mock_response.content = sample_sitemap_xml.encode()
        mock_response.headers = {}
        mock_response.status_code = 200
        
        with patch.object(parser.client, 'get', return_value=mock_response) as mock_get:
            mock_get.return_value.raise_for_status = MagicMock()
            urls = await parser.parse_sitemap_url("https://example.com/sitemap.xml")
            
            assert len(urls) == 2
            mock_get.assert_called_once()
        
        await parser.close()

    async def test_discover_sitemap_common_paths(self):
        """SEMANTIC: Test sitemap discovery from common paths."""
        parser = SitemapParser()
        
        # Mock successful response for sitemap.xml
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        with patch.object(parser.client, 'head', return_value=mock_response):
            sitemap_url = await parser.discover_sitemap("https://example.com")
            assert sitemap_url == "https://example.com/sitemap.xml"
        
        await parser.close()

    async def test_max_urls_limit(self):
        """SEMANTIC: Test that parser respects max URLs limit."""
        from src.core.config import settings
        
        # Create large sitemap
        urls_xml = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        for i in range(settings.MAX_URLS_PER_SITEMAP + 100):
            urls_xml += f'<url><loc>https://example.com/page{i}</loc></url>'
        urls_xml += '</urlset>'
        
        parser = SitemapParser()
        urls = parser.parse_sitemap_xml(urls_xml, "https://example.com")
        
        assert len(urls) <= settings.MAX_URLS_PER_SITEMAP
        await parser.close()
