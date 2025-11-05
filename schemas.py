from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DownloadHistoryBase(BaseModel):
    query: str
    filename: str
    service: str
    file_path: str
    file_size: Optional[float] = None

class DownloadHistoryCreate(DownloadHistoryBase):
    pass

class DownloadHistoryResponse(DownloadHistoryBase):
    id: int
    download_id: str
    download_time: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
