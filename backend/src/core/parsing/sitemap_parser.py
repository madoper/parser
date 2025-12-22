"""Sitemap XML parser for extracting URLs."""
# SEMANTIC: Parse XML sitemaps and extract URLs from nested indices
import logging
import gzip
from typing import List, Set, Optional, Dict
from urllib.parse import urljoin, urlparse
from datetime import datetime
import xml.etree.ElementTree as ET
import httpx

from src.core.config import settings

# SEMANTIC: Configure logging for parsing operations
logger = logging.getLogger(__name__)

# SEMANTIC: XML namespace for sitemap elements
NAMESPACES = {
    'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'image': 'http://www.google.com/schemas/sitemap-image/1.1',
    'video': 'http://www.google.com/schemas/sitemap-video/1.1',
}


class SitemapParser:
    """Parser for XML sitemaps and sitemap indices."""

    # SEMANTIC: Define supported sitemap content types
    SITEMAP_TYPES = {
        'urlset': 'url_sitemap',
        'sitemapindex': 'index_sitemap'
    }

    def __init__(self):
        """Initialize sitemap parser."""
        # SEMANTIC: Store discovered URLs and processed indices
        self.discovered_urls: Set[str] = set()
        self.processed_indices: Set[str] = set()
        
        # SEMANTIC: Initialize HTTP client with timeout and retries
        self.client = httpx.AsyncClient(
            timeout=settings.HTTP_TIMEOUT,
            follow_redirects=True,
            limits=httpx.Limits(max_keepalive_connections=20),
            headers={"User-Agent": settings.USER_AGENT}
        )

    async def parse_sitemap_url(self, url: str, max_depth: int = 3) -> List[str]:
        """Parse sitemap from URL and extract all URLs.
        
        Args:
            url: Sitemap or website URL
            max_depth: Maximum depth for nested sitemaps
            
        Returns:
            List of discovered URLs
        """
        # SEMANTIC: Initialize parsing session with depth tracking
        try:
            logger.info(f"Parsing sitemap from {url} (max_depth={max_depth})")
            
            # SEMANTIC: Fetch sitemap content
            response = await self.client.get(url)
            response.raise_for_status()
            
            # SEMANTIC: Handle gzipped content
            content = response.content
            if url.endswith('.gz') or response.headers.get('content-encoding') == 'gzip':
                content = await self.handle_gzip_sitemap(content)
                xml_content = content
            else:
                xml_content = response.text
            
            # SEMANTIC: Parse XML and determine sitemap type
            root = ET.fromstring(xml_content)
            tag = root.tag.split('}')[-1]  # Remove namespace
            
            if tag == 'sitemapindex':
                # SEMANTIC: Handle sitemap index (nested sitemaps)
                sitemap_urls = self._extract_sitemap_locations(root)
                logger.info(f"Found {len(sitemap_urls)} nested sitemaps in index")
                
                if max_depth > 0:
                    urls = await self.process_sitemap_index(sitemap_urls, max_depth - 1)
                else:
                    logger.warning(f"Max depth reached, skipping nested sitemaps")
                    urls = []
            else:
                # SEMANTIC: Handle regular sitemap with URLs
                urls = self.parse_sitemap_xml(xml_content, url)
                logger.info(f"Extracted {len(urls)} URLs from sitemap")
            
            # SEMANTIC: Update discovered URLs
            self.discovered_urls.update(urls)
            return urls
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching sitemap {url}: {e}")
            return []
        except ET.ParseError as e:
            logger.error(f"XML parse error for {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to parse sitemap {url}: {e}")
            return []

    def parse_sitemap_xml(self, xml_content: str, base_url: str) -> List[str]:
        """Parse XML sitemap content and extract URLs.
        
        Args:
            xml_content: XML content of sitemap
            base_url: Base URL for resolving relative links
            
        Returns:
            List of extracted URLs with metadata
        """
        # SEMANTIC: Parse XML and extract location URLs
        urls = []
        try:
            root = ET.fromstring(xml_content)
            
            # SEMANTIC: Extract all <loc> elements within <url> tags
            for url_elem in root.findall('.//ns:url', NAMESPACES):
                loc_elem = url_elem.find('ns:loc', NAMESPACES)
                if loc_elem is not None and loc_elem.text:
                    url = loc_elem.text.strip()
                    
                    # SEMANTIC: Resolve relative URLs
                    if not url.startswith(('http://', 'https://')):
                        url = urljoin(base_url, url)
                    
                    # SEMANTIC: Extract metadata
                    lastmod = url_elem.find('ns:lastmod', NAMESPACES)
                    changefreq = url_elem.find('ns:changefreq', NAMESPACES)
                    priority = url_elem.find('ns:priority', NAMESPACES)
                    
                    url_data = {
                        'url': url,
                        'lastmod': lastmod.text if lastmod is not None else None,
                        'changefreq': changefreq.text if changefreq is not None else None,
                        'priority': float(priority.text) if priority is not None else None,
                    }
                    
                    urls.append(url)
                    
                    # SEMANTIC: Check URL limit
                    if len(urls) >= settings.MAX_URLS_PER_SITEMAP:
                        logger.warning(f"Reached max URL limit ({settings.MAX_URLS_PER_SITEMAP})")
                        break
            
            logger.info(f"Parsed {len(urls)} URLs from XML")
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        
        return urls

    async def handle_gzip_sitemap(self, data: bytes) -> str:
        """Decompress gzipped sitemap data.
        
        Args:
            data: Gzipped binary data
            
        Returns:
            Decompressed XML content
        """
        # SEMANTIC: Handle compressed sitemap files (.gz)
        try:
            return gzip.decompress(data).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to decompress: {e}")
            raise

    async def process_sitemap_index(self, sitemaps: List[str], max_depth: int) -> List[str]:
        """Process sitemap index and recursively parse nested sitemaps.
        
        Args:
            sitemaps: List of sitemap URLs from index
            max_depth: Remaining depth for recursion
            
        Returns:
            Combined list of all discovered URLs
        """
        # SEMANTIC: Recursively follow nested sitemap indices
        all_urls = []
        
        for sitemap_url in sitemaps:
            # SEMANTIC: Skip already processed sitemaps
            if sitemap_url in self.processed_indices:
                logger.info(f"Skipping already processed sitemap: {sitemap_url}")
                continue
            
            self.processed_indices.add(sitemap_url)
            
            try:
                # SEMANTIC: Parse nested sitemap
                urls = await self.parse_sitemap_url(sitemap_url, max_depth)
                all_urls.extend(urls)
                
            except Exception as e:
                logger.error(f"Error parsing nested sitemap {sitemap_url}: {e}")
                continue
        
        return all_urls

    def _extract_sitemap_locations(self, root: ET.Element) -> List[str]:
        """Extract sitemap locations from sitemap index.
        
        Args:
            root: XML root element
            
        Returns:
            List of sitemap URLs
        """
        # SEMANTIC: Extract <loc> elements from <sitemap> tags
        locations = []
        for sitemap_elem in root.findall('.//ns:sitemap', NAMESPACES):
            loc_elem = sitemap_elem.find('ns:loc', NAMESPACES)
            if loc_elem is not None and loc_elem.text:
                locations.append(loc_elem.text.strip())
        return locations

    async def discover_sitemap(self, base_url: str) -> Optional[str]:
        """Discover sitemap URL from website.
        
        Args:
            base_url: Website base URL
            
        Returns:
            Discovered sitemap URL or None
        """
        # SEMANTIC: Try common sitemap locations
        common_paths = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemap.xml.gz',
            '/sitemap/sitemap.xml',
        ]
        
        parsed = urlparse(base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        for path in common_paths:
            sitemap_url = base + path
            try:
                response = await self.client.head(sitemap_url)
                if response.status_code == 200:
                    logger.info(f"Discovered sitemap at {sitemap_url}")
                    return sitemap_url
            except:
                continue
        
        # SEMANTIC: Try robots.txt
        try:
            robots_url = base + '/robots.txt'
            response = await self.client.get(robots_url)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if line.lower().startswith('sitemap:'):
                        sitemap_url = line.split(':', 1)[1].strip()
                        logger.info(f"Found sitemap in robots.txt: {sitemap_url}")
                        return sitemap_url
        except:
            pass
        
        logger.warning(f"Could not discover sitemap for {base_url}")
        return None

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
