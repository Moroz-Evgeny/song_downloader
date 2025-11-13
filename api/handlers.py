from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from api.utils.soundcloud import _search_song_with_soundcloud
from api.utils.general_utilits import _delete_file, _download_song, _create_history
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db, init_db
from schemas import DownloadHistoryCreate
from settings import DOWNLOADS_DIR
import os

download_router = APIRouter()

@download_router.on_event("startup")
async def startup_event():
    await init_db()

@download_router.get("/")
async def download_music(query: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    try:
        result = await _search_song_with_soundcloud(query)
        service = 'soundcloud'
        if not result:
            result = await _search_song_with_youtube(query)
            service = 'youtube'

        if not result:
            raise HTTPException(status_code=404, detail="Песня не найдена")

        safe_filename = result["safe_filename"]
        track_url = result["track_url"]
        filepath = os.path.join(DOWNLOADS_DIR, safe_filename)

        file_size = await _download_song(track_url, filepath)
        
        if file_size is None:
            raise HTTPException(status_code=500, detail="Ошибка при скачивании файла")

        download_data = DownloadHistoryCreate(
            query=query,
            filename=safe_filename,
            service=service,
            file_path=filepath,
            file_size=file_size,  
        )
        
        download_history = await _create_history(download_data=download_data, db=db)
        
        if download_history is None:
            print("Предупреждение: не удалось сохранить историю в БД")
        
        background_tasks.add_task(_delete_file, filepath)

        return FileResponse(filepath, media_type="audio/mpeg", filename=safe_filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


