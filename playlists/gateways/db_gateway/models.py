from datetime import datetime
from typing import Any

from sqlalchemy import Column, Date, DateTime, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from playlists.definitions import MusicProvider


Base: Any = declarative_base()


class SqlPlaylist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer(), primary_key=True)
    playlist_date = Column(Date(), nullable=False, index=True, unique=True)
    music_provider = Column(Enum(MusicProvider), nullable=False)
    music_provider_playlist_id = Column(String(32), nullable=False)

    created_at_utc = Column(DateTime(), nullable=False, default=datetime.utcnow)
    updated_on_utc = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
