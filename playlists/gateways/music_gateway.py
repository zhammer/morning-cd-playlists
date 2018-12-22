from typing import Dict, List
from urllib.parse import urlencode

import requests

from playlists.abc import MusicGateway as MusicGatewayABC
from playlists.definitions import (
    Listen,
    MusicProvider,
    MusicProviderPlaylist,
    MusicProviderPlaylistInput,
    Playlist,
    Song
)


class MusicGateway(MusicGatewayABC):
    auth_url = 'https://accounts.spotify.com/api/token'
    base_url = 'https://api.spotify.com/v1'

    def __init__(self, client_id: str, client_secret: str, refresh_token: str) -> None:
        """Refresh token requires scopes: ['playlist-modify-public']."""
        self.access_token = MusicGateway.fetch_access_token(client_id, client_secret, refresh_token)

    def create_playlist(self, playlist_input: MusicProviderPlaylistInput) -> MusicProviderPlaylist:
        r = requests.post(
            f'{self.base_url}/me/playlists',
            headers={'Authorization': f'Bearer {self.access_token}'},
            json=_build_create_playlist_body(playlist_input)
        )
        if not r.status_code == requests.codes.created:
            raise RuntimeError
        return _pluck_new_music_provider_playlist(r.json())

    def add_listen_to_playlist(self, listen: Listen, playlist: Playlist) -> None:
        r = requests.post(
            f'{self.base_url}/playlists/{playlist.music_provider_playlist_id}/tracks',
            headers={'Authorization': f'Bearer {self.access_token}'},
            params=_build_add_tracks_params(listen)
        )
        if not r.status_code == requests.codes.created:
            raise RuntimeError
        return None

    def fetch_playlist(self, playlist: Playlist) -> MusicProviderPlaylist:
        next_page = (f'{self.base_url}/playlists/{playlist.music_provider_playlist_id}/tracks?' +
                     urlencode({'fields': 'next,items(track(id))', 'limit': 100}))
        songs: List[Song] = []
        while next_page:
            r = requests.get(next_page, headers={'Authorization': f'Bearer {self.access_token}'})
            if not r.status_code == requests.codes.all_good:
                raise RuntimeError
            songs += _pluck_songs(r.json()['items'])
            next_page = r.json('next')

        return MusicProviderPlaylist(
            id=playlist.music_provider_playlist_id,
            music_provider=MusicProvider.SPOTIFY,
            songs=tuple(songs)
        )

    @staticmethod
    def fetch_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
        r = requests.post(
            auth=(client_id, client_secret),
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        return r.json()['access_token']


def _pluck_songs(raw_songs: Dict) -> List[Song]:
    return [Song(raw_song['track']['id']) for raw_song in raw_songs]


def _build_create_playlist_body(playlist_input: MusicProviderPlaylistInput) -> Dict:
    return {
        'name': playlist_input.name,
        'description': playlist_input.description,
        'public': True
    }


def _build_add_tracks_params(listen: Listen) -> Dict:
    return {'uris': f'spotify:track:{listen.song_id}'}


def _pluck_new_music_provider_playlist(raw_playlist: Dict) -> MusicProviderPlaylist:
    return MusicProviderPlaylist(
        id=raw_playlist['id'],
        music_provider=MusicProvider.SPOTIFY,
        songs=tuple()
    )
