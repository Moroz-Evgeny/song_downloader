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


def download_song_sync(track_url: str, filepath: str):
    try:
        base, _ = os.path.splitext(filepath)
        temp_path = base + ".%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'outtmpl': temp_path,
            'quiet': False,  # Включаем вывод для отладки
            'no_warnings': False,
            'ignoreerrors': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            },
        }

        print(f"Начинаем скачивание с SoundCloud: {track_url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Сначала получаем информацию о треке
            info = ydl.extract_info(track_url, download=False)
            print(f"Информация о треке: {info.get('title', 'Unknown')}")
            
            # Затем скачиваем
            ydl.download([track_url])

        # Ищем скачанный файл
        downloaded_file = None
        for f in os.listdir(os.path.dirname(filepath)):
            if f.startswith(os.path.basename(base)):
                downloaded_file = os.path.join(os.path.dirname(filepath), f)
                print(f"Найден файл: {downloaded_file}")
                # Если файл имеет другое имя, переименовываем
                if downloaded_file != filepath:
                    os.rename(downloaded_file, filepath)
                    print(f"Переименован в: {filepath}")
                break

        if os.path.exists(filepath):
            file_size_bytes = os.path.getsize(filepath)
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_size_mb_rounded = round(file_size_mb, 2)
            print(f"Файл успешно скачан: {filepath}, размер: {file_size_mb_rounded} МБ")
            return file_size_mb_rounded
        else:
            print("Файл не был создан после скачивания")
            # Пробуем найти любой файл в директории
            all_files = os.listdir(os.path.dirname(filepath))
            print(f"Файлы в директории: {all_files}")
            return None
            
    except Exception as e:
        print(f'Ошибка скачивания SoundCloud: {e}')
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