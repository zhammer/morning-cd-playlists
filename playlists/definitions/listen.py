from datetime import date
from typing import NamedTuple

from playlists.definitions import MusicProvider


class Listen(NamedTuple):
    id: str
    song_id: str
    listen_date: date
    song_provider: MusicProvider
