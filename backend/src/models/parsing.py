"""Pydantic models for parsing operations."""
# SEMANTIC: Data models for sitemap parsing and task management
from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """SEMANTIC: Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SitemapRequest(BaseModel):
    """SEMANTIC: Request model for sitemap parsing."""
    url: HttpUrl = Field(..., description="Sitemap or website URL to parse")
    max_depth: Optional[int] = Field(3, ge=1, le=10, description="Maximum depth for nested sitemaps")
    follow_nested: Optional[bool] = Field(True, description="Follow nested sitemap indices")
    save_to_db: Optional[bool] = Field(True, description="Save results to database")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/sitemap.xml",
                "max_depth": 3,
                "follow_nested": True,
                "save_to_db": True,
            }
        }


class ParsedURL(BaseModel):
    """SEMANTIC: Parsed URL with metadata."""
    url: str = Field(..., description="The parsed URL")
    lastmod: Optional[datetime] = Field(None, description="Last modification date")
    changefreq: Optional[str] = Field(None, description="Change frequency")
    priority: Optional[float] = Field(None, ge=0.0, le=1.0, description="Priority value")
    status_code: Optional[int] = Field(None, description="HTTP status code if fetched")
    content_type: Optional[str] = Field(None, description="Content type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/page",
                "lastmod": "2024-01-15T10:30:00",
                "changefreq": "weekly",
                "priority": 0.8,
            }
        }


class SitemapResponse(BaseModel):
    """SEMANTIC: Response model for sitemap parsing."""
    task_id: str = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(..., description="Current task status")
    total_urls: int = Field(0, ge=0, description="Total number of URLs discovered")
    urls: Optional[List[str]] = Field(default_factory=list, description="List of discovered URLs")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Task creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "total_urls": 150,
                "urls": ["https://example.com/page1", "https://example.com/page2"],
                "created_at": "2024-01-15T10:30:00",
            }
        }


class ParsingTask(BaseModel):
    """SEMANTIC: Complete parsing task model for database storage."""
    id: str = Field(..., description="Unique task identifier")
    url: str = Field(..., description="Source URL")
    status: TaskStatus = Field(..., description="Task status")
    config: Dict[str, Any] = Field(..., description="Task configuration")
    result: Optional[Dict[str, Any]] = Field(None, description="Parsing results")
    error: Optional[str] = Field(None, description="Error message")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    @validator('config')
    def validate_config(cls, v):
        """SEMANTIC: Validate configuration dictionary."""
        required_keys = ['max_depth', 'follow_nested']
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required config key: {key}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "url": "https://example.com/sitemap.xml",
                "status": "completed",
                "config": {"max_depth": 3, "follow_nested": True},
                "result": {"total_urls": 150, "processed": 150},
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:35:00",
                "completed_at": "2024-01-15T10:35:00",
            }
        }


class PageContent(BaseModel):
    """SEMANTIC: Extracted page content and metadata."""
    url: str = Field(..., description="Page URL")
    title: Optional[str] = Field(None, description="Page title")
    description: Optional[str] = Field(None, description="Meta description")
    keywords: Optional[str] = Field(None, description="Meta keywords")
    text_content: Optional[str] = Field(None, description="Extracted text content")
    content_length: int = Field(0, description="Content length in bytes")
    status_code: int = Field(..., description="HTTP status code")
    fetched_at: datetime = Field(..., description="Fetch timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/page",
                "title": "Example Page",
                "description": "This is an example page",
                "keywords": "example, demo, test",
                "text_content": "Page content...",
                "content_length": 1024,
                "status_code": 200,
                "fetched_at": "2024-01-15T10:30:00",
            }
        }


class TaskListResponse(BaseModel):
    """SEMANTIC: Response for listing tasks."""
    tasks: List[ParsingTask] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    page: int = Field(1, ge=1, description="Current page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
            }
        }


class HealthCheck(BaseModel):
    """SEMANTIC: Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "0.1.0",
                "timestamp": "2024-01-15T10:30:00",
            }
        }
