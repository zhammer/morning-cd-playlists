from datetime import date

from playlists.definitions import MusicProvider
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


@given('a playlist exists for "{playlist_date}"')
def step_impl(context, playlist_date):
    sql_playlist = SqlPlaylist(
        playlist_date=date.fromisoformat(playlist_date),
        music_provider=MusicProvider.SPOTIFY,
        music_provider_playlist_id=DEFAULT_MUSIC_PROVIDER_PLAYLIST_ID
    )
    context.session.add(sql_playlist)
    context.session.commit()


@given('a playlist doesn\'t exist for "{playlist_date}"')
def step_impl(context, playlist_date):
    query = context.session.query(SqlPlaylist)
    query = query.filter(SqlPlaylist.playlist_date == date.fromisoformat(playlist_date))
    assert not query.first()


@given('the spotify playlist has the tracks')
def step_impl(context):
    context.spotify_playlist_song_ids = [row['song_id'] for row in context.table]


@when('playlists receives an add-listen-to-playlist message')
def step_impl(context):
    raise NotImplementedError('STEP: When playlists receives an add-listen-to-playlist message')


@then('there is a playlist for "{playlist_date}"')
def step_impl(context, playlist_date):
    query = context.session.query(SqlPlaylist)
    query = query.filter(SqlPlaylist.playlist_date == date.fromisoformat(playlist_date))
    assert query.first()


@then('the song id "41wel0JyLABRedko4XZLG1" has been added to the corresponding spotify playlist')
def step_impl(context):
    raise NotImplementedError('STEP: Then the song id "41wel0JyLABRedko4XZLG1" has been added to the corresponding spotify playlist')


@then('the song id "0kJ4CyjZJT0P4caqKYG4jZ" has been added to the corresponding spotify playlist')
def step_impl(context):
    raise NotImplementedError('STEP: Then the song id "0kJ4CyjZJT0P4caqKYG4jZ" has been added to the corresponding spotify playlist')


@when('playlists received an add-listen-to-playlist message')
def step_impl(context):
    raise NotImplementedError('STEP: When playlists received an add-listen-to-playlist message')


@then('the song id "0kJ4CyjZJT0P4caqKYG4jZ" has not been added to the corresponding spotify playlist')
def step_impl(context):
    raise NotImplementedError('STEP: Then the song id "0kJ4CyjZJT0P4caqKYG4jZ" has not been added to the corresponding spotify playlist')
