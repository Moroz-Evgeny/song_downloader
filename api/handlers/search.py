from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from fastapi.responses import FileResponse
import httpx
from api.utils.soundcloud import get_access_token, _search_song_with_soundcloud
from api.utils.general_utilits import _delete_file, _download_song, _create_history
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db, init_db
from schemas import DownloadHistoryCreate
from settings import DOWNLOADS_DIR
import os

search_router = APIRouter()

@search_router.get("/search")
async def search_tracks(query: str, limit: int = 50):
    """
    Поиск только доступных для потокового воспроизведения треков
    """
    result = await _search_song_with_soundcloud(query=query, limit=limit)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис поиска временно недоступен"
        )

    return result