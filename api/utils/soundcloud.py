import time
from fastapi import HTTPException
import os, asyncio, base64, httpx
from typing import Union
from settings import API_URL, CLIENT_ID, CLIENT_SECRET, TOKEN_URL

access_token_cache = None
token_expires_at = 0

async def get_access_token() -> str:
    """Получение токена через Client Credentials Flow с проверкой срока действия"""
    global access_token_cache, token_expires_at
    
    # Проверяем, есть ли валидный токен (с запасом в 5 минут)
    if access_token_cache and time.time() < token_expires_at - 300:
        return access_token_cache

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = base64.b64encode(auth_str.encode()).decode()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            headers={
                "Authorization": f"Basic {auth_bytes}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"grant_type": "client_credentials"},
        )

    if response.status_code != 200:
        print(f"Token request failed: {response.status_code} - {response.text}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to obtain access token from SoundCloud"
        )

    data = response.json()
    access_token_cache = data["access_token"]
    
    # Устанавливаем время истечения токена (обычно 2 часа)
    token_expires_at = time.time() + data.get("expires_in", 7200)
    
    print(f"Successfully obtained new access token, expires at: {token_expires_at}")
    return access_token_cache

async def _search_song_with_soundcloud(query: str, limit: int) -> Union[dict, None]:
    """
    Поиск только доступных для потокового воспроизведения треков
    """
    try:
        token = await get_access_token()

        params = {
            "q": query,
            "limit": limit,
            "linked_partitioning": "true",
            "access": "playable"  # Только треки доступные для воспроизведения
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_URL}/tracks",
                headers={"Authorization": f"OAuth {token}"},
                params=params,
            )

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

# async def _search_song_with_soundcloud(query: str) -> Union[dict, None]:
#     """Асинхронная обёртка для поиска на SoundCloud"""
#     return await asyncio.to_thread(search_song_with_soundcloud_sync, query)

async def _get_stream_url_with_soundcloud(track_id: int) -> Union[dict, None]:
    """
    Получение URL для потокового воспроизведения трека
    """
    print(f"Getting stream URL for track {track_id}")
    
    try:
        token = await get_access_token()

        # Сначала получаем информацию о треке
        async with httpx.AsyncClient() as client:
            track_resp = await client.get(
                f"{API_URL}/tracks/{track_id}",
                headers={"Authorization": f"OAuth {token}"},
            )

        if track_resp.status_code != 200:
            print(f"SoundCloud track API error: {track_resp.status_code} - {track_resp.text}")
            return None

        track_data = track_resp.json()
        print(f"Track data: {track_data}")

        # Проверяем доступность трека
        if track_data.get("access") != "playable":
            print(f"Track {track_id} is not available for streaming")
            return None

        # Получаем stream URL через официальный endpoint
        async with httpx.AsyncClient(follow_redirects=False) as client:
            stream_resp = await client.get(
                f"{API_URL}/tracks/{track_id}/stream",
                headers={"Authorization": f"OAuth {token}"},
            )

        print(f"Stream response status: {stream_resp.status_code}")
        print(f"Stream response headers: {dict(stream_resp.headers)}")

        if stream_resp.status_code == 302:  # Редирект
            # Получаем реальный MP3 URL из заголовка Location
            stream_url = stream_resp.headers.get('location')
            if not stream_url:
                print(f"No redirect location found for track {track_id}")
                return None
        elif stream_resp.status_code == 200:
            # Если нет редиректа, парсим JSON
            stream_data = stream_resp.json()
            stream_url = stream_data.get("url")
            if not stream_url:
                print(f"No stream URL in response for track {track_id}")
                return None
        else:
            print(f"SoundCloud stream API error: {stream_resp.status_code} - {stream_resp.text}")
            return None

        # Теперь получаем финальный URL (может быть еще один редирект)
        async with httpx.AsyncClient(follow_redirects=False) as client:
            final_resp = await client.get(stream_url)
            
            if final_resp.status_code == 302:
                final_url = final_resp.headers.get('location')
            else:
                final_url = stream_url

        if not final_url:
            print(f"No final stream URL available for track {track_id}")
            return None

        # Обрабатываем артворк
        artwork_url = track_data.get("artwork_url")
        if artwork_url:
            artwork_url = artwork_url.replace("large", "t500x500")

        return {
            "stream_url": final_url,
            "track_info": {
                "title": track_data.get("title") or "Unknown Title",
                "artist": track_data.get("user", {}).get("username") or "Unknown Artist",
                "permalink_url": track_data.get("permalink_url"),
                "artist_permalink": track_data.get("user", {}).get("permalink_url"),
                "artwork": artwork_url
            }
        }
    
    except httpx.HTTPError as e:
        print(f"HTTP error during SoundCloud stream retrieval: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during SoundCloud stream retrieval: {e}")
        return None