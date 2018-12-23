from contextlib import contextmanager
from datetime import date
from typing import List

from behave import given, then, when

import responses

from features.fixtures import listens as listens_fixtures
from features.fixtures import spotify as spotify_fixtures

from playlists.definitions import MusicProvider
from playlists.delivery.sqs_consumer import consumer as add_listen_to_playlist_consumer
from playlists.gateways.db_gateway.models import SqlPlaylist


DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID = '3jLuwmR6Fx0bEKbaSu9V6B'


@given('a listen has just been created with the fields')
def step_impl(context):
    context.new_listen_fields = {
        'id': context.table[0]['id'],
        'song_id': context.table[0]['song_id'],
        'listen_time_utc': context.table[0]['listen_time_utc'],
        'song_provider': context.table[0]['song_provider']
    }


@given('a playlist exists for "{playlist_date}"')  # noqa: F811
def step_impl(context, playlist_date):
    sql_playlist = SqlPlaylist(
        playlist_date=date.fromisoformat(playlist_date),
        music_provider=MusicProvider.SPOTIFY,
        music_provider_playlist_id=DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID
    )
    context.session.add(sql_playlist)
    context.session.commit()


@given('a playlist doesn\'t exist for "{playlist_date}"')  # noqa: F811
def step_impl(context, playlist_date):
    query = context.session.query(SqlPlaylist)
    query = query.filter(SqlPlaylist.playlist_date == date.fromisoformat(playlist_date))
    assert not query.first()


@given('the spotify playlist has the tracks')  # noqa: F811
def step_impl(context):
    context.spotify_playlist_song_ids = [row['song_id'] for row in context.table]


@when('playlists receives an add-listen-to-playlist message')  # noqa: F811
def step_impl(context):
    listen_id = context.new_listen_fields['id']
    event = {'Records': [{'body': f'{{"listen_id": "{listen_id}"}}'}]}

    with playlists_mock_network(context) as mock_network:
        add_listen_to_playlist_consumer(event=event, context={})
        context.mock_calls = steal_mock_calls(mock_network)


@then('there is a playlist for "{playlist_date}"')  # noqa: F811
def step_impl(context, playlist_date):
    query = context.session.query(SqlPlaylist)
    query = query.filter(SqlPlaylist.playlist_date == date.fromisoformat(playlist_date))
    sql_playlist = query.first()
    assert sql_playlist.playlist_date == date.fromisoformat(playlist_date)
    assert sql_playlist.music_provider_playlist_id == DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID


@then('the song id "{id}" has been added to the corresponding spotify playlist')  # noqa: F811
def step_impl(context, id):
    # should be taken care of by mock network with querystring matching
    pass


@then('the song id "{id}" has not been added to the corresponding spotify playlist')  # noqa: F811
def step_impl(context, id):
    # should be taken care of by mock network omitting add tracks calls
    pass


PLAYLIST_DOESNT_EXIST_SCENARIO = "A playlist doesn't exist for the listen's submit date"
PLAYLIST_EXISTS_WITHOUT_LISTEN = ("A playlist exists for the listen's submit date, and the listen "
                                  "hasn't been submitted")
PLAYLIST_EXISTS_WITH_LISTEN = ("A playlist exists for the listen's submit date, and the listen has "
                               "already been submitted")


def steal_mock_calls(mock_network: responses.RequestsMock) -> List[responses.Call]:
    """Steals mock calls from a responses.RequestsMock before they're destroyed at contextmanager
    exit.
    """
    return [mock_network.calls[i] for i in range(len(mock_network.calls))]


@contextmanager
def playlists_mock_network(context):
    scenario_name = context.scenario.name
    if scenario_name == PLAYLIST_DOESNT_EXIST_SCENARIO:
        with responses.RequestsMock() as mock_network:
            mock_network.add(spotify_fixtures.make_post_refresh_token())
            mock_network.add(listens_fixtures.make_listen_response(**context.new_listen_fields))
            mock_network.add(
                spotify_fixtures.make_create_playlist(DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID)
            )
            mock_network.add(
                spotify_fixtures.make_get_playlist(DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID, [])
            )
            mock_network.add(
                spotify_fixtures.make_add_track_to_playlist(
                    DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID,
                    context.new_listen_fields['song_id'])
            )
            yield mock_network
    elif scenario_name == PLAYLIST_EXISTS_WITHOUT_LISTEN:
        with responses.RequestsMock() as mock_network:
            mock_network.add(spotify_fixtures.make_post_refresh_token())
            mock_network.add(listens_fixtures.make_listen_response(**context.new_listen_fields))
            mock_network.add(spotify_fixtures.make_get_playlist(
                DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID,
                context.spotify_playlist_song_ids)
            )
            mock_network.add(spotify_fixtures.make_add_track_to_playlist(
                DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID,
                context.new_listen_fields['song_id'])
            )
            yield mock_network
    elif scenario_name == PLAYLIST_EXISTS_WITH_LISTEN:
        with responses.RequestsMock() as mock_network:
            mock_network.add(spotify_fixtures.make_post_refresh_token())
            mock_network.add(listens_fixtures.make_listen_response(**context.new_listen_fields))
            mock_network.add(spotify_fixtures.make_get_playlist(
                DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID,
                context.spotify_playlist_song_ids)
            )
            yield mock_network
        pass
    else:
        raise RuntimeError(
            f'Trying to setup a mockenv for an unknown scenario: {context.scenario.name}'
        )
