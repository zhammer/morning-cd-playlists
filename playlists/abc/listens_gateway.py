from abc import ABC, abstractmethod

from playlists.definitions import Listen


class ListensGateway(ABC):

    @abstractmethod
    def fetch_listen(self, listen_id: str) -> Listen:
        ...
