import os, yt_dlp, asyncio
import time
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
            # Кэшировать результаты
            'cachedir': '/tmp/yt_dlp_cache',
            # Случайные задержки
            'sleep_interval': random.randint(1, 3),
            'max_sleep_interval': 5,
        }

        # Пробуем несколько раз с разными настройками
        for attempt in range(3):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                break
            except Exception as e:
                if attempt == 2:  # последняя попытка
                    raise e
                print(f"Попытка {attempt + 1} не удалась, пробуем снова...")
                time.sleep(2)


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