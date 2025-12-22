"""Parsing service for web scraping operations."""
# SEMANTIC: Core service for parsing sitemaps and URLs
import asyncio
import logging
from typing import List, Optional, Set, Dict
from datetime import datetime
from uuid import uuid4
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from src.core.parsing.sitemap_parser import SitemapParser
from src.core.config import settings
from src.core.database import get_collection, Collections

# SEMANTIC: Configure logging for parsing operations
logger = logging.getLogger(__name__)


class ParsingService:
    """Service for handling sitemap and webpage parsing."""

    def __init__(self):
        """Initialize parsing service."""
        # SEMANTIC: Store parsed URLs in memory cache
        self.parsed_urls: Set[str] = set()
        self.tasks: Dict[str, Dict] = {}
        
        # SEMANTIC: Initialize HTTP client
        self.client = httpx.AsyncClient(
            timeout=settings.HTTP_TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": settings.USER_AGENT}
        )

    async def parse_sitemap(self, url: str, max_depth: int = 3) -> Dict[str, any]:
        """Parse sitemap URL and extract all URLs.
        
        Args:
            url: Sitemap or website URL to parse
            max_depth: Maximum depth for nested sitemap indices
            
        Returns:
            Dictionary with parsing results
        """
        # SEMANTIC: Initialize URL collection for parsing session
        result = {
            "url": url,
            "urls": [],
            "total_urls": 0,
            "status": "success",
            "error": None,
            "started_at": datetime.utcnow(),
            "completed_at": None,
        }
        
        try:
            logger.info(f"Starting sitemap parsing for {url}")
            
            # SEMANTIC: Create parser instance
            parser = SitemapParser()
            
            # SEMANTIC: Check if URL is a sitemap or website
            if url.endswith('.xml') or url.endswith('.xml.gz') or 'sitemap' in url.lower():
                # SEMANTIC: Parse sitemap directly
                urls = await parser.parse_sitemap_url(url, max_depth)
            else:
                # SEMANTIC: Discover sitemap from website
                sitemap_url = await parser.discover_sitemap(url)
                if sitemap_url:
                    urls = await parser.parse_sitemap_url(sitemap_url, max_depth)
                else:
                    logger.warning(f"No sitemap found for {url}, crawling homepage")
                    urls = [url]
            
            # SEMANTIC: Store results
            result["urls"] = urls
            result["total_urls"] = len(urls)
            result["completed_at"] = datetime.utcnow()
            
            # SEMANTIC: Update parsed URLs cache
            self.parsed_urls.update(urls)
            
            logger.info(f"Successfully parsed {len(urls)} URLs from {url}")
            
            # SEMANTIC: Close parser
            await parser.close()
            
        except Exception as e:
            logger.error(f"Error parsing sitemap: {e}", exc_info=True)
            result["status"] = "error"
            result["error"] = str(e)
            result["completed_at"] = datetime.utcnow()
        
        return result

    async def extract_urls_from_html(self, html: str, base_url: str) -> List[str]:
        """Extract URLs from HTML content.
        
        Args:
            html: HTML content to parse
            base_url: Base URL for resolving relative links
            
        Returns:
            List of extracted URLs
        """
        # SEMANTIC: Parse HTML and extract links using CSS selectors
        urls = set()
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # SEMANTIC: Extract all <a> tags with href
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # SEMANTIC: Skip anchors, javascript, and mailto links
                if href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                    continue
                
                # SEMANTIC: Resolve relative URLs
                absolute_url = urljoin(base_url, href)
                
                # SEMANTIC: Filter by domain (same domain only)
                base_domain = urlparse(base_url).netloc
                url_domain = urlparse(absolute_url).netloc
                
                if url_domain == base_domain:
                    urls.add(absolute_url)
            
            logger.info(f"Extracted {len(urls)} URLs from HTML")
            
        except Exception as e:
            logger.error(f"Error extracting URLs from HTML: {e}")
        
        return list(urls)

    async def fetch_page_content(self, url: str) -> Optional[Dict[str, any]]:
        """Fetch and parse webpage content.
        
        Args:
            url: URL to fetch
            
        Returns:
            Dictionary with page content and metadata
        """
        try:
            # SEMANTIC: Fetch page with timeout
            response = await self.client.get(url)
            response.raise_for_status()
            
            # SEMANTIC: Parse HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # SEMANTIC: Extract metadata
            title = soup.find('title')
            description = soup.find('meta', attrs={'name': 'description'})
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            
            # SEMANTIC: Extract main content
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            result = {
                "url": url,
                "status_code": response.status_code,
                "title": title.string if title else None,
                "description": description['content'] if description else None,
                "keywords": keywords['content'] if keywords else None,
                "text_content": text[:5000],  # Limit to 5000 chars
                "content_length": len(response.text),
                "fetched_at": datetime.utcnow(),
            }
            
            logger.info(f"Successfully fetched content from {url}")
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching page content: {e}")
            return None

    def create_task(self, url: str, config: Dict) -> Dict:
        """Create new parsing task.
        
        Args:
            url: URL to parse
            config: Task configuration
            
        Returns:
            Task metadata
        """
        # SEMANTIC: Generate unique task ID
        task_id = str(uuid4())
        
        # SEMANTIC: Store task state for monitoring
        task = {
            "id": task_id,
            "url": url,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "config": config,
            "result": None,
            "error": None,
        }
        
        self.tasks[task_id] = task
        logger.info(f"Created parsing task {task_id} for {url}")
        
        return task

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get status of parsing task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task status and results
        """
        # SEMANTIC: Retrieve task status from task registry
        task = self.tasks.get(task_id)
        
        if task:
            return {
                "id": task["id"],
                "status": task["status"],
                "created_at": task["created_at"],
                "updated_at": task["updated_at"],
                "result": task.get("result"),
                "error": task.get("error"),
            }
        
        return None

    def update_task_status(self, task_id: str, status: str, result: any = None, error: str = None):
        """Update task status.
        
        Args:
            task_id: Task identifier
            status: New status
            result: Task result data
            error: Error message if failed
        """
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            self.tasks[task_id]["updated_at"] = datetime.utcnow()
            
            if result is not None:
                self.tasks[task_id]["result"] = result
            
            if error is not None:
                self.tasks[task_id]["error"] = error
            
            logger.info(f"Updated task {task_id} status to {status}")

    async def save_parsing_results(self, task_id: str, urls: List[str], metadata: Dict):
        """Save parsing results to database.
        
        Args:
            task_id: Task identifier
            urls: List of parsed URLs
            metadata: Additional metadata
        """
        try:
            # SEMANTIC: Get MongoDB collection
            collection = get_collection(Collections.PARSING_TASKS)
            
            # SEMANTIC: Prepare document
            document = {
                "task_id": task_id,
                "urls": urls,
                "total_urls": len(urls),
                "metadata": metadata,
                "created_at": datetime.utcnow(),
            }
            
            # SEMANTIC: Insert into database
            result = await collection.insert_one(document)
            logger.info(f"Saved parsing results for task {task_id}: {result.inserted_id}")
            
        except Exception as e:
            logger.error(f"Error saving parsing results: {e}")

    async def close(self):
        """Close HTTP client and cleanup resources."""
        await self.client.aclose()
        logger.info("Parsing service closed")
