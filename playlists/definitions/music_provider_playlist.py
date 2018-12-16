from typing import NamedTuple, Tuple

from playlists.definitions import MusicProvider, Song


class MusicProviderPlaylist(NamedTuple):
    id: str
    music_provider: MusicProvider
    songs: Tuple[Song, ...]
