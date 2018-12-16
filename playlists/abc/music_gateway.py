from abc import ABC, abstractmethod

from playlists.definitions import Listen, MusicProviderPlaylist, Playlist


class MusicGateway(ABC):

    @abstractmethod
    def create_playlist(self, description: str) -> MusicProviderPlaylist:
        ...

    @abstractmethod
    def add_listen_to_playlist(self, listen: Listen, playlist: Playlist) -> None:
        ...
