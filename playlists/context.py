from typing import NamedTuple

from playlists.abc import (
    DbGateway as DbGatewayABC,
    ListensGateway as ListensGatewayABC,
    MusicGateway as MusicGatewayABC
)


class Context(NamedTuple):
    db_gateway: DbGatewayABC
    listens_gateway: ListensGatewayABC
    music_gateway: MusicGatewayABC
