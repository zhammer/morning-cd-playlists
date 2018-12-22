from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from playlists.definitions import MusicProviderPlaylist, Playlist


class DbGateway(ABC):

    @abstractmethod
    def fetch_playlist_by_date(self, playlist_date: date) -> Optional[Playlist]:
        ...

    @abstractmethod
    def create_playlist(self, music_provider_playlist: MusicProviderPlaylist,
                        playlist_date: date) -> Playlist:
        ...
