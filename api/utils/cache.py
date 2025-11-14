from cachetools import TTLCache
import redis
import asyncio
from typing import Any, Optional
import time
from settings import REDIS_URL

# In-memory кэш для часто запрашиваемых данных
search_cache = TTLCache(maxsize=1000, ttl=300)  # 5 минут для поиска
stream_cache = TTLCache(maxsize=500, ttl=1800)  # 30 минут для stream URL

# Redis клиент для распределенного кэширования и rate limiting
redis_client = None

try:
    if REDIS_URL:
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        # Тестируем подключение
        redis_client.ping()
except Exception as e:
    print(f"Redis connection failed: {e}. Using in-memory cache only.")
    redis_client = None

class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
    
    async def is_rate_limited(self, identifier: str) -> bool:
        """Проверяет, превышен ли лимит запросов"""
        if not redis_client:
            return False
            
        key = f"rate_limit:{identifier}"
        try:
            current = redis_client.get(key)
            if current is None:
                redis_client.setex(key, self.window, 1)
                return False
            if int(current) >= self.requests:
                return True
            redis_client.incr(key)
            return False
        except Exception as e:
            print(f"Rate limiting error: {e}")
            return False

class CacheManager:
    @staticmethod
    async def get_search_cache(query: str, limit: int) -> Optional[Any]:
        """Получить результаты поиска из кэша"""
        cache_key = f"search:{query}:{limit}"
        
        # Сначала проверяем in-memory кэш
        if cache_key in search_cache:
            return search_cache[cache_key]
        
        # Затем проверяем Redis
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    # Сохраняем в in-memory кэш для быстрого доступа
                    search_cache[cache_key] = cached
                    return cached
            except Exception as e:
                print(f"Redis get error: {e}")
        
        return None

    @staticmethod
    async def set_search_cache(query: str, limit: int, data: Any):
        """Сохранить результаты поиска в кэш"""
        cache_key = f"search:{query}:{limit}"
        
        # Сохраняем в in-memory кэш
        search_cache[cache_key] = data
        
        # Сохраняем в Redis
        if redis_client:
            try:
                redis_client.setex(cache_key, 300, data)  # 5 минут
            except Exception as e:
                print(f"Redis set error: {e}")

    @staticmethod
    async def get_stream_cache(track_id: int) -> Optional[Any]:
        """Получить stream URL из кэша - ТОЛЬКО МЕТАДАННЫЕ, без stream_url"""
        cache_key = f"stream_meta:{track_id}"
        
        if cache_key in stream_cache:
            return stream_cache[cache_key]
            
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    stream_cache[cache_key] = cached
                    return cached
            except Exception as e:
                print(f"Redis get error: {e}")
        
        return None

    @staticmethod
    async def set_stream_cache(track_id: int, data: Any):
        """Сохранить МЕТАДАННЫЕ трека в кэш (без stream_url)"""
        cache_key = f"stream_meta:{track_id}"
        
        # Удаляем stream_url из данных для кэширования
        if isinstance(data, dict) and 'stream_url' in data:
            cache_data = data.copy()
            del cache_data['stream_url']
        else:
            cache_data = data
        
        stream_cache[cache_key] = cache_data
        
        if redis_client:
            try:
                redis_client.setex(cache_key, 3600, json.dumps(cache_data))  # 1 час для метаданных
            except Exception as e:
                print(f"Redis set error: {e}")

# Инициализация rate limiter'ов
search_limiter = RateLimiter(requests=30, window=60)    # 30 запросов в минуту
stream_limiter = RateLimiter(requests=50, window=60)    # 50 запросов в минуту