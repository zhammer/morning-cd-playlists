import os

from playlists.context import Context
from playlists.gateways import DbGateway, ListensGateway, MusicGateway


def create_default_context() -> Context:
    database_connection_string = os.environ['DATABASE_CONNECTION_STRING']
    listens_service_api_key = os.environ['LISTENS_SERVICE_API_KEY']
    spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
    spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    spotify_user_refresh_token = os.environ['SPOTIFY_USER_REFRESH_TOKEN']

    return Context(
        db_gateway=DbGateway(database_connection_string),
        listens_gateway=ListensGateway(listens_service_api_key),
        music_gateway=MusicGateway(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            refresh_token=spotify_user_refresh_token
        )
    )
