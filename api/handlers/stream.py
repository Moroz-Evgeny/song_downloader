from fastapi import APIRouter, HTTPException, Request, status
from api.utils.soundcloud import _get_stream_url_with_soundcloud
from api.utils.cache import CacheManager, stream_limiter
import json

stream_router = APIRouter()

@stream_router.get("/stream/{track_id}")
async def stream_track(request: Request, track_id: int):
    """
    Получение URL для потокового воспроизведения
    с кэшированием и rate limiting
    """
    # Проверяем rate limiting
    client_ip = request.client.host
    if await stream_limiter.is_rate_limited(f"stream:{client_ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много запросов потокового воспроизведения. Пожалуйста, подождите."
        )
    
    # Проверяем кэш
    cached_result = await CacheManager.get_stream_cache(track_id)
    if cached_result:
        return json.loads(cached_result)
    
    # Получаем stream URL
    result = await _get_stream_url_with_soundcloud(track_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Трек не найден или недоступен для потокового воспроизведения"
        )
    
    # Сохраняем в кэш
    await CacheManager.set_stream_cache(track_id, json.dumps(result))
    
    return result