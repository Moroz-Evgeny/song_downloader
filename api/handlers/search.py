from fastapi import APIRouter, HTTPException, Request, status
from api.utils.soundcloud import _search_song_with_soundcloud
from api.utils.cache import CacheManager, search_limiter
import json

search_router = APIRouter()

@search_router.get("/search")
async def search_tracks(request: Request, query: str, limit: int = 50):
    """
    Поиск только доступных для потокового воспроизведения треков
    с кэшированием и rate limiting
    """
    # Проверяем rate limiting
    client_ip = request.client.host
    if await search_limiter.is_rate_limited(f"search:{client_ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много запросов поиска. Пожалуйста, подождите."
        )
    
    # Ограничиваем максимальный лимит
    if limit > 50:
        limit = 50
    
    # Проверяем кэш
    cached_result = await CacheManager.get_search_cache(query, limit)
    if cached_result:
        return json.loads(cached_result)
    
    # Выполняем поиск
    result = await _search_song_with_soundcloud(query=query, limit=limit)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис поиска временно недоступен"
        )
    
    # Сохраняем в кэш
    await CacheManager.set_search_cache(query, limit, json.dumps(result))
    
    return result