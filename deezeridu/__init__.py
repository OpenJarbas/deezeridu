#!/usr/bin/python3

from .api import API
from .gateway import Gateway
from .download import (
    TrackDownloader, AlbumDownloader, PlaylistDownloader,
    DownloaderJob
)

from .utils import (
    create_zip, get_ids, link_is_valid,
    what_kind, convert_to_date
)
from .exceptions import (
    InvalidLink, TrackNotFound,
    NoDataApi, AlbumNotFound
)
from .models import (
    Track, Album, Playlist,
    Preferences, Smart
)


class Deezer:
    def __init__(
            self,
            arl=None,
            email=None,
            password=None
    ):
        if arl:
            self.__gw_api = Gateway(arl=arl)
        else:
            self.__gw_api = Gateway(
                email=email,
                password=password
            )

        self.__api = API()
        self.__download_job = DownloaderJob(self.__api, self.__gw_api)

    def download_track(
            self, link_track,
            output_dir,
            quality_download="MP3_320",
            recursive_quality=False,
            recursive_download=False,
            not_interface=False,
            method_save=2
    ) -> Track:

        link_is_valid(link_track)
        ids = get_ids(link_track)

        try:
            song_metadata = self.__api.tracking(ids)
        except NoDataApi:
            infos = self.__gw_api.get_song_data(ids)

            if not "FALLBACK" in infos:
                raise TrackNotFound(link_track)

            ids = infos['FALLBACK']['SNG_ID']
            song_metadata = self.__api.tracking(ids)

        preferences = Preferences()

        preferences.link = link_track
        preferences.song_metadata = song_metadata
        preferences.quality_download = quality_download
        preferences.output_dir = output_dir
        preferences.ids = ids
        preferences.recursive_quality = recursive_quality
        preferences.recursive_download = recursive_download
        preferences.not_interface = not_interface
        preferences.method_save = method_save

        track = TrackDownloader(preferences, self.__download_job).dw()

        return track

    def download_album(
            self, link_album,
            output_dir,
            quality_download="MP3_320",
            recursive_quality=False,
            recursive_download=False,
            not_interface=False,
            make_zip=False,
            method_save=2
    ) -> Album:

        link_is_valid(link_album)
        ids = get_ids(link_album)

        try:
            album_json = self.__api.get_album(ids)
        except NoDataApi:
            raise AlbumNotFound(link_album)

        song_metadata = {
            "music": [],
            "artist": [],
            "tracknum": [],
            "discnum": [],
            "bpm": [],
            "duration": [],
            "isrc": [],
            "gain": [],
            "album": album_json['title'],
            "label": album_json['label'],
            "year": convert_to_date(album_json['release_date']),
            "upc": album_json['upc'],
            "nb_tracks": album_json['nb_tracks']
        }

        genres = []

        if "genres" in album_json:
            for a in album_json['genres']['data']:
                genres.append(a['name'])

        song_metadata['genre'] = " & ".join(genres)
        ar_album = []

        for a in album_json['contributors']:
            if a['role'] == "Main":
                ar_album.append(a['name'])

        song_metadata['ar_album'] = " & ".join(ar_album)
        sm_items = song_metadata.items()

        for track in album_json['tracks']['data']:
            c_ids = track['id']
            detas = self.__api.tracking(c_ids, album=True)

            for key, item in sm_items:
                if type(item) is list:
                    song_metadata[key].append(detas[key])

        preferences = Preferences()

        preferences.link = link_album
        preferences.song_metadata = song_metadata
        preferences.quality_download = quality_download
        preferences.output_dir = output_dir
        preferences.ids = ids
        preferences.json_data = album_json
        preferences.recursive_quality = recursive_quality
        preferences.recursive_download = recursive_download
        preferences.not_interface = not_interface
        preferences.method_save = method_save
        preferences.make_zip = make_zip

        album = AlbumDownloader(preferences, self.__download_job).dw()

        return album

    def download_playlist(
            self, link_playlist,
            output_dir,
            quality_download="MP3_320",
            recursive_quality=False,
            recursive_download=False,
            not_interface=False,
            make_zip=False,
            method_save=2
    ) -> Playlist:

        link_is_valid(link_playlist)
        ids = get_ids(link_playlist)

        song_metadata = []
        playlist_json = self.__api.get_playlist(ids)

        for track in playlist_json['tracks']['data']:
            c_ids = track['id']

            try:
                c_song_metadata = self.__api.tracking(c_ids)
            except NoDataApi:
                infos = self.__gw_api.get_song_data(c_ids)

                if not "FALLBACK" in infos:
                    c_song_metadata = f"{track['title']} - {track['artist']['name']}"
                else:
                    c_song_metadata = self.__api.tracking(c_ids)

            song_metadata.append(c_song_metadata)

        preferences = Preferences()

        preferences.link = link_playlist
        preferences.song_metadata = song_metadata
        preferences.quality_download = quality_download
        preferences.output_dir = output_dir
        preferences.ids = ids
        preferences.json_data = playlist_json
        preferences.recursive_quality = recursive_quality
        preferences.recursive_download = recursive_download
        preferences.not_interface = not_interface
        preferences.method_save = method_save
        preferences.make_zip = make_zip

        playlist = PlaylistDownloader(preferences, self.__download_job).dw()

        return playlist

    def download_artist_toptracks(
            self, link_artist,
            output_dir,
            quality_download="MP3_320",
            recursive_quality=False,
            recursive_download=False,
            not_interface=False
    ):

        link_is_valid(link_artist)
        ids = get_ids(link_artist)

        playlist_json = self.__api.get_artist_top_tracks(ids)['data']

        names = [
            self.download_track(
                track['link'], output_dir,
                quality_download, recursive_quality,
                recursive_download, not_interface
            )

            for track in playlist_json
        ]
        return Playlist(names)

    def download(
            self, link,
            output_dir,
            quality_download="MP3_320",
            recursive_quality=False,
            recursive_download=False,
            not_interface=False,
            make_zip=False,
            method_save=2
    ) -> Smart:

        link_is_valid(link)
        link = what_kind(link)
        smart = Smart()

        if "deezer.com" in link:
            source = "https://deezer.com"

        smart.source = source

        if "first_result/" in link:
            if "deezer.com" in link:
                func = self.download_track

            else:
                raise InvalidLink(link)

            track = func(
                link,
                output_dir=output_dir,
                quality_download=quality_download,
                recursive_quality=recursive_quality,
                recursive_download=recursive_download,
                not_interface=not_interface,
                method_save=2
            )

            smart.type = "first_result"
            smart._track = track

        elif "album/" in link:
            if "deezer.com" in link:
                func = self.download_album

            else:
                raise InvalidLink(link)

            album = func(
                link,
                output_dir=output_dir,
                quality_download=quality_download,
                recursive_quality=recursive_quality,
                recursive_download=recursive_download,
                not_interface=not_interface,
                make_zip=make_zip,
                method_save=2
            )

            smart.type = "album"
            smart._album = album
        elif "artist/" in link:
            if "deezer.com" in link:
                func = self.download_artist_toptracks
            else:
                raise InvalidLink(link)

            playlist = func(
                link,
                output_dir=output_dir,
                quality_download=quality_download,
                recursive_quality=recursive_quality,
                recursive_download=recursive_download,
                not_interface=not_interface
            )
            smart.type = "playlist"
            smart._playlist = playlist

        elif "playlist/" in link:
            if "deezer.com" in link:
                func = self.download_playlist

            else:
                raise InvalidLink(link)

            playlist = func(
                link,
                output_dir=output_dir,
                quality_download=quality_download,
                recursive_quality=recursive_quality,
                recursive_download=recursive_download,
                not_interface=not_interface,
                make_zip=make_zip,
                method_save=2
            )

            smart.type = "playlist"
            smart._playlist = playlist

        return smart
