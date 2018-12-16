from typing import NamedTuple

from playlists.definitions import MusicProvider


class MusicProviderPlaylist(NamedTuple):
    id: str
    music_provider: MusicProvider
