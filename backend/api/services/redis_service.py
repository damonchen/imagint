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

    @staticmethod
    def rpush(key: str, value: str) -> bool:
        """
        Push value to Redis list
        Args:
            key: Redis key
            value: Value to push
        Returns:
            True if successful
        """
        try:
            return redis_client.rpush(key, value)
        except Exception as e:
            logger.error(f"Failed to push value to Redis list: {e}")
            raise

    @staticmethod
    def lpop(key: str) -> str:
        """
        Pop value from Redis list
        """
        try:
            return redis_client.lpop(key)
        except Exception as e:
            logger.error(f"Failed to pop value from Redis list: {e}")
            raise

    @staticmethod
    def lrange(key: str, start: int, end: int) -> list[str]:
        """
        Get values from Redis list
        """
        try:
            return redis_client.lrange(key, start, end)
        except Exception as e:
            logger.error(f"Failed to get values from Redis list: {e}")
            raise
