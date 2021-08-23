#!/usr/bin/python3


class Playlist:
    def __init__(self) -> None:
        self.__t_list = []
        self.zip_path = None

    @property
    def tracks(self):
        return self.__t_list
