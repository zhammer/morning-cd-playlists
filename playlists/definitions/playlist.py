from datetime import date
from typing import NamedTuple

from playlists.definitions import MusicProvider


class Playlist(NamedTuple):
    id: str
    playlist_date: date
    music_provider_playlist_id: str
    music_provider: MusicProvider
