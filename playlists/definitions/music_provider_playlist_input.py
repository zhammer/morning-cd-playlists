from typing import NamedTuple

from playlists.definitions import MusicProvider


class MusicProviderPlaylistInput(NamedTuple):
    name: str
    description: str
    music_provider: MusicProvider
