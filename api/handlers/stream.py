from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from api.utils.soundcloud import get_access_token, _search_song_with_soundcloud, _get_stream_url_with_soundcloud
from api.utils.general_utilits import _delete_file, _download_song, _create_history
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db, init_db
from schemas import DownloadHistoryCreate
from settings import DOWNLOADS_DIR
import os

stream_router = APIRouter()

@stream_router.get("/stream/{track_id}")
async def stream_track(track_id: int):
    """
    Получение URL для потокового воспроизведения
    """
    result = await _get_stream_url_with_soundcloud(track_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Трек не найден или недоступен для потокового воспроизведения"
        )
    
    return result