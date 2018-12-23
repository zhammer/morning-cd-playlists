from responses import Response


def make_listen_response(id: str,
                         song_id: str,
                         listen_time_utc: str,
                         song_provider: str) -> Response:
    return Response(
        method='GET',
        url=f'https://micro.morningcd.com/listens/{id}',
        json={
            'id': id,
            'song_id': song_id,
            'listen_time_utc': listen_time_utc,
            'song_provider': song_provider
        }
    )
