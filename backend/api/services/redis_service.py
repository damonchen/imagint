import logging
from api.extensions.redis import redis_client

logger = logging.getLogger(__name__)


class RedisService(object):
    @staticmethod
    def get(key: str) -> bytes:
        """
        Get value from Redis by key
        Args:
            key: Redis key
        Returns:
            Value in bytes
        """
        try:
            return redis_client.get(key)
        except Exception as e:
            logger.error(f"Failed to get value from Redis: {e}")
            raise

    @staticmethod
    def set(key: str, value: bytes, ex: int = None) -> bool:
        """
        Set key-value pair to Redis
        Args:
            key: Redis key
            value: Value to set
            ex: Expiration time in seconds
        Returns:
            True if successful
        """
        try:
            return redis_client.set(key, value, ex=ex)
        except Exception as e:
            logger.error(f"Failed to set value to Redis: {e}")
            raise

    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete key from Redis
        Args:
            key: Redis key
        Returns:
            True if successful
        """
        try:
            return redis_client.delete(key)
        except Exception as e:
            logger.error(f"Failed to delete key from Redis: {e}")
            raise

    @staticmethod
    def exists(key: str) -> bool:
        """
        Check if key exists in Redis
        Args:
            key: Redis key
        Returns:
            True if key exists
        """
        try:
            return redis_client.exists(key)
        except Exception as e:
            logger.error(f"Failed to check key existence in Redis: {e}")
            raise
