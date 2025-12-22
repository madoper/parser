"""MongoDB database connection and lifecycle management."""
# SEMANTIC: Async MongoDB connection with motor driver
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from src.core.config import settings

# SEMANTIC: Configure logging for database operations
logger = logging.getLogger(__name__)

# SEMANTIC: Global MongoDB client instance
_mongodb_client: Optional[AsyncIOMotorClient] = None
_mongodb_database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> None:
    """SEMANTIC: Establish MongoDB connection on application startup.
    
    Creates connection pool with configured min/max pool sizes.
    Connection is reused across all requests.
    """
    global _mongodb_client, _mongodb_database
    
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
        
        # SEMANTIC: Create async MongoDB client with connection pooling
        _mongodb_client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
            maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            serverSelectionTimeoutMS=5000,
        )
        
        # SEMANTIC: Test connection with ping command
        await _mongodb_client.admin.command('ping')
        
        # SEMANTIC: Get database instance
        _mongodb_database = _mongodb_client[settings.MONGODB_DB_NAME]
        
        logger.info(f"Successfully connected to MongoDB database: {settings.MONGODB_DB_NAME}")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection() -> None:
    """SEMANTIC: Close MongoDB connection on application shutdown.
    
    Properly closes connection pool and releases resources.
    """
    global _mongodb_client
    
    if _mongodb_client:
        try:
            logger.info("Closing MongoDB connection")
            _mongodb_client.close()
            logger.info("MongoDB connection closed successfully")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
    else:
        logger.warning("MongoDB client was not initialized")


def get_database() -> AsyncIOMotorDatabase:
    """SEMANTIC: Get MongoDB database instance for dependency injection.
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database instance
        
    Raises:
        RuntimeError: If database is not initialized
    """
    if _mongodb_database is None:
        raise RuntimeError(
            "Database not initialized. Call connect_to_mongo() first."
        )
    return _mongodb_database


def get_collection(collection_name: str):
    """SEMANTIC: Get specific collection from database.
    
    Args:
        collection_name: Name of the collection to retrieve
        
    Returns:
        Collection instance
    """
    db = get_database()
    return db[collection_name]


# SEMANTIC: Collection name constants
class Collections:
    """SEMANTIC: Centralized collection name definitions."""
    PARSING_TASKS = "parsing_tasks"
    PARSED_URLS = "parsed_urls"
    SITEMAP_CACHE = "sitemap_cache"
    USER_SESSIONS = "user_sessions"
