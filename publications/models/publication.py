
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime

from config.database import Base

class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
