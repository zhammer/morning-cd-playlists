from typing import List

from responses import Response


def make_post_refresh_token() -> Response:
    return Response(
        method='POST',
        url='https://accounts.spotify.com/api/token',
        json={
            'access_token': 'MockSpotifyAccessToken'
        }
    )


def make_create_playlist(id: str) -> Response:
    return Response(
        method='POST',
        url='https://api.spotify.com/v1/me/playlists',
        status=201,
        json={'id': id}
    )


def make_get_playlist(id: str, song_ids: List[str]) -> Response:
    return Response(
        method='GET',
        url=f'https://api.spotify.com/v1/playlists/{id}/tracks',
        match_querystring=False,
        json={
            'items': [{'track': {'id': song_id}} for song_id in song_ids],
            'next': None
        }
    )


def make_add_track_to_playlist(id: str, song_id: str) -> Response:
    return Response(
        method='POST',
        url=f'https://api.spotify.com/v1/playlists/{id}/tracks?uris=spotify%3Atrack%3A{song_id}',
        status=201
    )
