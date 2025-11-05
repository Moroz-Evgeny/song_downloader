from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class DownloadHistory(Base):
    __tablename__ = "download_history"
    
    id = Column(Integer, primary_key=True, index=True)
    download_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    query = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    service = Column(String(50), nullable=False)  # 'youtube' или 'soundcloud'
    file_path = Column(Text, nullable=False)
    file_size = Column(Float, nullable=True) 
    download_time = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DownloadHistory {self.download_id} - {self.filename}>"