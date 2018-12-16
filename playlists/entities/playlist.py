import random
from datetime import date

from playlists.definitions import MusicProviderPlaylistInput


def make_music_provider_playlist_input(for_date) -> MusicProviderPlaylistInput:
    return MusicProviderPlaylistInput(
        description=_make_playlist_description(for_date),
        name=_make_playlist_description(for_date)
    )


def _make_playlist_description(for_date: date) -> str:
    """
    >>> _make_playlist_description(for_date=date(1994, 4, 26))
    'Listens submitted to morning cd on 1994-04-26.'
    """
    return f'Listens submitted to morning cd on {for_date}.'


def _make_playlist_name(for_date: date) -> str:
    """
    >>> playlist_name = _make_playlist_name(for_date=date(1994, 4, 26))
    >>> start, middle, end = playlist_name.split('~')
    >>> start in EMOJIS and end in EMOJIS and not start == end
    True
    >>> middle
    'morning cd 1994-04-26'
    """
    start_emoji, end_emoji = random.sample(EMOJIS, 2)
    return f'{start_emoji}~morning cd {for_date}~{end_emoji}'


BLOSSOM = '\U0001F33C'
GLOWING_STAR = '\U0001F31F'
HERB = '\U0001F33F'
MAPLE_LEAF = '\U0001F341'
RABBIT = '\U0001F407'
SEEDLING = '\U0001F331'
SNOWFLAKE = '\U00002744\U0000FE0F'
SNOW_CAPPED_MOUNTAIN = '\U0001F3D4\U0000FE0F'
SPEAKER_HIGH_VOLUME = '\U0001F50A'
WATER_WAVE = '\U0001F30A'


EMOJIS = {
    BLOSSOM,
    GLOWING_STAR,
    HERB,
    MAPLE_LEAF,
    RABBIT,
    SEEDLING,
    SNOWFLAKE,
    SNOW_CAPPED_MOUNTAIN,
    SPEAKER_HIGH_VOLUME,
    WATER_WAVE
}
