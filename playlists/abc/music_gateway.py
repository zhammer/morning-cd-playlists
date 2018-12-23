from abc import ABC, abstractmethod

from playlists.definitions import (
    Listen,
    MusicProviderPlaylist,
    MusicProviderPlaylistInput,
    Playlist
)


class MusicGateway(ABC):

    @abstractmethod
    def create_playlist(self, playlist_input: MusicProviderPlaylistInput) -> MusicProviderPlaylist:
        ...

    @abstractmethod
    def add_listen_to_playlist(self, listen: Listen, playlist: Playlist) -> None:
        ...

    @abstractmethod
    def fetch_playlist(self, playlist: Playlist) -> MusicProviderPlaylist:
        ...
