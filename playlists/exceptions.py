class PlaylistsException(Exception):
    """Base exception for playlists service."""


class ListensError(PlaylistsException):
    """Exception raised upon ecnountering an error with the listens service."""


class MusicProviderError(PlaylistsException):
    """Exception raised upon encountering an error with the music provider."""
