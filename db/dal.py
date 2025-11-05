from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, and_
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import os

from db.models import DownloadHistory
from schemas import DownloadHistoryCreate

class DownloadHistoryDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_download_record(self, download_data: DownloadHistoryCreate) -> DownloadHistory:
        try:
            db_download = DownloadHistory(**download_data.dict())
            self.db_session.add(db_download)
            await self.db_session.commit()
            await self.db_session.refresh(db_download)
            return db_download
        except Exception as e:
            await self.db_session.rollback()
            raise e









