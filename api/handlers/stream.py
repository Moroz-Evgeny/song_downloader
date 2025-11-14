from fastapi import APIRouter, HTTPException, Request, status
from api.utils.soundcloud import _get_stream_url_with_soundcloud
from api.utils.cache import CacheManager, stream_limiter
import json

stream_router = APIRouter()

@stream_router.get("/stream/{track_id}")
async def stream_track(request: Request, track_id: int):
    """
    Получение URL для потокового воспроизведения
    Кэшируем только метаданные, stream_url получаем каждый раз свежий
    """
    print(f"Stream request for track_id: {track_id}")
    
    # Проверяем rate limiting
    client_ip = request.client.host
    if await stream_limiter.is_rate_limited(f"stream:{client_ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много запросов потокового воспроизведения. Пожалуйста, подождите."
        )
    
    # Проверяем кэш ТОЛЬКО для метаданных
    cached_meta = await CacheManager.get_stream_cache(track_id)
    
    # Всегда получаем свежий stream_url
    result = await _get_stream_url_with_soundcloud(track_id)
    
    if not result:
        # Если трек не найден, но есть кэшированные метаданные - все равно возвращаем ошибку
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Трек не найден или недоступен для потокового воспроизведения"
        )
    
    # Если есть кэшированные метаданные, объединяем их со свежим stream_url
    if cached_meta:
        print(f"Using cached metadata for track {track_id}")
        # Сохраняем свежий stream_url, но используем кэшированные метаданные
        final_result = json.loads(cached_meta)
        final_result['stream_url'] = result['stream_url']
    else:
        # Сохраняем метаданные в кэш (без stream_url)
        await CacheManager.set_stream_cache(track_id, json.dumps({
            'track_info': result.get('track_info', {})
        }))
        final_result = result
    
    print(f"Returning fresh stream URL for track {track_id}")
    return final_result