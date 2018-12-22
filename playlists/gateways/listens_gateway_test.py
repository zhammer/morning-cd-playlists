import os
from datetime import date

from faaspact_maker import (
    Interaction,
    PactMaker,
    ProviderState,
    RequestWithMatchers,
    ResponseWithMatchers,
    matchers
)

import pytest

from playlists import exceptions
from playlists.definitions import Listen, MusicProvider
from playlists.gateways import ListensGateway


PACT_DIRECTORY = os.environ.get('PACT_DIRECTORY', 'pacts')


class TestFetchListen:

    def test_fetches_listen_by_id(self) -> None:
        # Given a listens service gateway
        listens_service_gateway = ListensGateway(api_key='xyz')

        # And this pact with the listens service
        listen_fields = {
            'id': '1',
            'song_id': '41wel0JyLABRedko4XZLG1',
            'listen_date': '2018-11-04T15:04:49.987156',
            'song_provider': 'SPOTIFY'
        }
        pact = PactMaker(
            'playlists', 'listens', 'https://micro.morningcd.com',
            pact_directory=PACT_DIRECTORY
        )
        pact.add_interaction(Interaction(
            description='a request for a listen',
            provider_states=(ProviderState(
                name='a listen exists with the fields',
                params={'fields': listen_fields}),
            ),
            request=RequestWithMatchers(
                method='GET',
                path='/listens/1'
            ),
            response=ResponseWithMatchers(
                status=200,
                body=listen_fields
            )
        ))

        # When we request a listen from the listens service
        with pact.start_mocking():
            listen = listens_service_gateway.fetch_listen('1')

        # Then we get the listen from the listens service
        expected_listen = Listen(
            id='1',
            song_id='41wel0JyLABRedko4XZLG1',
            listen_date=date(2018, 11, 4),
            song_provider=MusicProvider.SPOTIFY
        )
        assert listen == expected_listen

    def test_raises_exception_if_listen_doesnt_exist(self) -> None:
        # Given a listens service gateway
        listens_service_gateway = ListensGateway(api_key='xyz')

        # And this pact with the listens service
        pact = PactMaker(
            'playlists', 'listens', 'https://micro.morningcd.com',
            pact_directory=PACT_DIRECTORY
        )
        pact.add_interaction(Interaction(
            description='a request for a listen',
            provider_states=(ProviderState('there are no listens in the database'),),
            request=RequestWithMatchers(
                method='GET',
                path='/listens/1'
            ),
            response=ResponseWithMatchers(
                status=404,
                body={'message': matchers.Like('No listen exists with id 1')}
            )
        ))

        # When we request a listen from the listens service
        with pact.start_mocking():
            with pytest.raises(exceptions.ListensError):
                listens_service_gateway.fetch_listen('1')
