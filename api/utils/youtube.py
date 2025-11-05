import os, yt_dlp, asyncio
from typing import Union
from ytmusicapi import YTMusic
from settings import DOWNLOADS_DIR

ytmusic = YTMusic()


import os
import asyncio
from typing import Union
from settings import DOWNLOADS_DIR

def search_song_with_youtube_sync(query: str) -> Union[dict, None]:
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
            'no_warnings': True,
            'ignoreerrors': True,
            'proxy': 'socks5://nY5CwB:ZcMEw6@45.130.129.232:8000',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'params': {'client_id': 'i1WGJflNesCYHVXqGUzw4whCQc1NXnWGzapNVbAOZy'}
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            
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
        print(f"Ошибка поиска YouTube: {e}")
        return None

async def _search_song_with_youtube(query: str) -> Union[dict, None]:
    return await asyncio.to_thread(search_song_with_youtube_sync, query)





