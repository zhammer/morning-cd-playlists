from datetime import date, datetime
from typing import Dict

import requests

from playlists import exceptions
from playlists.abc import ListensGateway as ListensGatewayABC
from playlists.definitions import Listen, MusicProvider


class ListensGateway(ListensGatewayABC):
    base_url = 'https://micro.morningcd.com/listens'

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def fetch_listen(self, listen_id: str) -> Listen:
        r = requests.get(f'{self.base_url}/{listen_id}', headers={
            'Authorization': f'Bearer {self.api_key}'
        })
        if not r.status_code == requests.codes.all_good:
            raise exceptions.ListensError('Error communicating with the listens service: '
                                          f'{r.json()["message"]}')
        return _pluck_listen(r.json())


def _pluck_listen(raw_listen: Dict) -> Listen:
    return Listen(
        id=raw_listen['id'],
        song_id=raw_listen['song_id'],
        song_provider=MusicProvider[raw_listen['song_provider']],
        listen_date=_pluck_date(raw_listen['listen_time_utc']),
    )


def _pluck_date(datetime_string: str) -> date:
    """
    >>> _pluck_date('2018-11-04T15:04:49.987156')
    datetime.date(2018, 11, 4)
    """
    return datetime.fromisoformat(datetime_string).date()
