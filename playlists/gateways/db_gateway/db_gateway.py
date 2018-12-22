from datetime import date
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from playlists.abc import DbGateway as DbGatewayABC
from playlists.definitions import MusicProviderPlaylist, Playlist
from playlists.gateways.db_gateway.models import Base, SqlPlaylist


class DbGateway(DbGatewayABC):

    def __init__(self, db_name: str, echo: bool = False) -> None:
        self.engine = create_engine(db_name, echo=echo)
        self.session = sessionmaker(bind=self.engine)()

    def fetch_playlist_by_date(self, playlist_date: date) -> Optional[Playlist]:
        query = self.session.query(SqlPlaylist).filter(SqlPlaylist.date == playlist_date)
        sql_playlist = query.first()
        return sql_playlist and _pluck_playlist(sql_playlist)

    def create_playlist(self, music_provider_playlist: MusicProviderPlaylist,
                        playlist_date: date) -> Playlist:
        sql_playlist = _build_sql_playlist(music_provider_playlist, playlist_date)
        self.session.add(sql_playlist)
        self.session.commit()
        return _pluck_playlist(sql_playlist)

    def persist_schema(self) -> None:
        """Not part of DbGatewayABC."""
        Base.metadata.create_all(self.engine)


def _build_sql_playlist(music_provider_playlist: MusicProviderPlaylist,
                        playlist_date: date) -> SqlPlaylist:
    return SqlPlaylist(
        playlist_date=playlist_date,
        music_provider=music_provider_playlist.music_provider,
        music_provider_playlist_id=music_provider_playlist.id
    )


def _pluck_playlist(sql_playlist: SqlPlaylist) -> Playlist:
    return Playlist(
        id=sql_playlist.id,
        playlist_date=sql_playlist.playlist_date,
        music_provider_playlist_id=sql_playlist.music_provider_playlist_id,
        music_provider=sql_playlist.music_provider
    )
