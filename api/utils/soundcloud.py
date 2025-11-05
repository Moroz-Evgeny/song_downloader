import os, yt_dlp, asyncio
from typing import Union
from settings import DOWNLOADS_DIR

def search_song_with_soundcloud_sync(query: str) -> Union[dict, None]:
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'default_search': 'scsearch',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"scsearch:{query}", download=False)
            
            if not info or 'entries' not in info or not info['entries']:
                return None
            
            track = info['entries'][0]
            title = track.get('title', 'Unknown Title')
            artist = track.get('uploader', 'Unknown Artist')
            track_url = track.get('url', '')
            
            filename = f"{artist} - {title}.mp3"
            safe_filename = "".join(c for c in filename if c.isalnum() or c in " .-_()").strip()
            
            return {
                "safe_filename": safe_filename,
                "track_url": track_url,
                "title": title,
                "artist": artist
            }
    
    except Exception as e:
        print(f"Ошибка поиска SoundCloud: {e}")
        return None

async def _search_song_with_soundcloud(query: str) -> Union[dict, None]:
    """Асинхронная обёртка для поиска на SoundCloud"""
    return await asyncio.to_thread(search_song_with_soundcloud_sync, query)
