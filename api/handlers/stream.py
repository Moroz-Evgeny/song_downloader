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
    print(f"Stream request for track_id: {track_id}")
    
    # Проверяем rate limiting
    client_ip = request.client.host
    if await stream_limiter.is_rate_limited(f"stream:{client_ip}"):
        print(f"Rate limited for IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много запросов потокового воспроизведения. Пожалуйста, подождите."
        )
    
    # Проверяем кэш
    cached_result = await CacheManager.get_stream_cache(track_id)
    if cached_result:
        print(f"Cache HIT for track {track_id}")
        result = json.loads(cached_result)
        print(f"Cached result: {result}")
        return result
    
    print(f"Cache MISS for track {track_id}")
    # Получаем stream URL
    result = await _get_stream_url_with_soundcloud(track_id)
    
    if not result:
        print(f"Track {track_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Трек не найден или недоступен для потокового воспроизведения"
        )
    
    print(f"API result: {result}")
    
    # Сохраняем в кэш
    await CacheManager.set_stream_cache(track_id, json.dumps(result))
    
    return result