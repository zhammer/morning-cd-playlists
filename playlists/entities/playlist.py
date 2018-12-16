from datetime import date


def make_playlist_description(for_date: date) -> str:
    """
    >>> make_playlist_description(for_date=date(1994, 4, 26))
    'Listens submitted to morning cd on 1994-04-26.'
    """
    return f'Listens submitted to morning cd on {for_date}.'
