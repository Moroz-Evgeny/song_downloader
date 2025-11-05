import os, yt_dlp, asyncio
from typing import Union
from ytmusicapi import YTMusic
from settings import DOWNLOADS_DIR

ytmusic = YTMusic()


def search_song_with_youtube_sync(query: str) -> Union[dict, None]:
    try:
        results = ytmusic.search(query, filter="songs")
        if not results:
            return None
        
        first_song = results[0]
        videoId = first_song.get("videoId")
        title = first_song.get("title", "Unknown Title")
        artist = first_song["artists"][0]["name"] if first_song.get("artists") else "Unknown Artist"
        filename = f"{artist} - {title}.mp3"

        safe_filename = "".join(c for c in filename if c.isalnum() or c in " .-_()").strip()
        track_url = f"https://music.youtube.com/watch?v={videoId}"
        
        return {
            "safe_filename": safe_filename,
            "track_url": track_url
            }
    except Exception as e:
        print(f'Ошибка поиска Youtube: {e}')
        return None

async def _search_song_with_youtube(query: str) -> Union[dict, None]:
    return await asyncio.to_thread(search_song_with_youtube_sync, query)






