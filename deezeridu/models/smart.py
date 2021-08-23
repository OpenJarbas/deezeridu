#!/usr/bin/python3

from .album import Album
from .playlist import Playlist
from .track import Track


class Smart:
    def __init__(self) -> None:
        self._track = None
        self._album = None
        self._playlist = None
        self.type = None
        self.source = None

    @property
    def track(self) -> Track:
        return self._track

    @property
    def album(self) -> Album:
        return self._album

    @property
    def playlist(self) -> Playlist:
        return self._playlist
