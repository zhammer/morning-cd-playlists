from playlists.context import Context
from playlists.definitions import Listen, Playlist
from playlists.entities import playlist as playlist_entity


def add_listen_to_playlist(context: Context, listen_id: str) -> None:
    """Adds a listen to the morning cd playlist for the day the listen was submitted.
    If a playlist for the listen's submitted date doesn't exist, create the playlist.
    Note: This use case in its current state doesn't support parallel runs.
    """
    listen = context.listens_gateway.fetch_listen(listen_id)
    playlist = context.db_gateway.fetch_playlist_by_date(listen.listen_date)
    if not playlist:
        playlist = create_playlist_for_listen(context, listen)
    music_provider_playlist = context.music_gateway.fetch_playlist(playlist)
    if listen.song_id not in (song.id for song in music_provider_playlist.songs):
        context.music_gateway.add_listen_to_playlist(listen, playlist)


def create_playlist_for_listen(context: Context, listen: Listen) -> Playlist:
    music_provider_playlist_input = playlist_entity.make_music_provider_playlist_input(
        for_date=listen.listen_date,
        music_provider=listen.song_provider
    )
    music_provider_playlist = context.music_gateway.create_playlist(music_provider_playlist_input)
    return context.db_gateway.create_playlist(music_provider_playlist, listen.listen_date)
