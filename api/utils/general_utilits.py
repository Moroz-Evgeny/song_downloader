import os, yt_dlp, asyncio
from schemas import DownloadHistoryCreate
from sqlalchemy.ext.asyncio import AsyncSession
from db.dal import DownloadHistoryDAL
from db.models import DownloadHistory

def _delete_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"Файл удалён: {path}")
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")


def download_song_sync(video_url: str, filepath: str):
    try:
        base, _ = os.path.splitext(filepath)
        temp_path = base + ".%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'outtmpl': temp_path,
            'quiet': True,
            # Пробуем разные подходы
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls'],
                }
            },
            # Форсируем использование определенных экстракторов
            'allowed_extractors': ['youtube', 'generic'],
            # Добавляем задержки между запросами
            'sleep_interval': 2,
            'max_sleep_interval': 5,
        }


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Ищем и переименовываем файл
        for f in os.listdir(os.path.dirname(filepath)):
            if f.startswith(os.path.basename(base)) and not f.endswith(".mp3"):
                temp_file_path = os.path.join(os.path.dirname(filepath), f)
                os.rename(temp_file_path, filepath)
                break

        # Проверяем существование файла после переименования
        if os.path.exists(filepath):
            file_size_bytes = os.path.getsize(filepath)
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_size_mb_rounded = round(file_size_mb, 2)
            return file_size_mb_rounded
        else:
            print("Файл не был создан после скачивания")
            return None
            
    except Exception as e:
        print(f'Ошибка скачивания Youtube: {e}')
        return None

async def _download_song(video_url: str, filepath: str):
    file_size = await asyncio.to_thread(download_song_sync, video_url, filepath)
    return file_size


async def _create_history(download_data: DownloadHistoryCreate, db: AsyncSession) -> DownloadHistory:
  try:
    dal = DownloadHistoryDAL(db)
    record = await dal.create_download_record(download_data)
    return record
  except Exception as e:
      print(f'Ошибка сохранения в бд: {e}')
      return None