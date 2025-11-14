from fastapi import APIRouter, HTTPException, Request, status
from api.utils.soundcloud import _search_song_with_soundcloud
from api.utils.cache import CacheManager, search_limiter
import json

search_router = APIRouter()

async def _search_song_with_soundcloud(query: str, limit: int) -> Union[dict, None]:
    """
    Поиск только доступных для потокового воспроизведения треков
    с повторными попытками при 401 ошибке
    """
    max_retries = 2
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            token = await get_access_token()

            params = {
                "q": query,
                "limit": limit,
                "linked_partitioning": "true",
                "access": "playable"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{API_URL}/tracks",
                    headers={"Authorization": f"OAuth {token}"},
                    params=params,
                )

            if response.status_code == 401:
                print(f"SoundCloud API unauthorized (attempt {retry_count + 1}/{max_retries + 1})")
                # Инвалидируем токен и пробуем снова
                global access_token_cache, token_expires_at
                access_token_cache = None
                token_expires_at = 0
                retry_count += 1
                continue
                
            if response.status_code != 200:
                print(f"SoundCloud API error: {response.status_code} - {response.text}")
                return None

            data = response.json()
        
            if isinstance(data, dict):
                if "collection" in data:
                    data = data["collection"]
                elif "errors" in data: 
                    print(f"SoundCloud API errors: {data.get('errors')}")
                    return None
            
            if not isinstance(data, list):
                print(f"Unexpected data format: {type(data)}")
                return None

            tracks = []
            for t in data:
                if isinstance(t, dict) and t.get("access") == "playable" and t.get("id"):
                    artwork_url = t.get("artwork_url")
                    if artwork_url:
                        artwork_url = artwork_url.replace("large", "t500x500")
                    
                    tracks.append({
                        "id": t.get("id"),
                        "title": t.get("title") or "Unknown Title",
                        "artist": t.get("user", {}).get("username") or "Unknown Artist",
                        "artist_permalink": t.get("user", {}).get("permalink_url"),
                        "genre": t.get("genre"),
                        "artwork": artwork_url,
                        "permalink_url": t.get("permalink_url"),
                        "duration": t.get("duration", 0),
                        "access": t.get("access"),
                    })

            return {"results": tracks}
        
        except httpx.HTTPError as e:
            print(f"HTTP error during SoundCloud search: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during SoundCloud search: {e}")
            return None
    
    print(f"All {max_retries + 1} attempts failed with 401 Unauthorized")
    return None