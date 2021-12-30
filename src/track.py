# track.py

from file_handler import write_bytes_to_cache, delete_file
from requests import get
from string import whitespace


class NoLyricsException(Exception):
    pass


class Track:
    def __init__(self, track_json: dict[str], added_date: str):
        # Parse track json to init Track.
        self._saved_on = added_date;
        self._name = track_json["name"];
        self._album = track_json["album"]["name"];
        self._album_art = write_bytes_to_cache(
            self._album,
            get(track_json["album"]["images"][0]["url"]).content
        );
        self._artists = [artist["name"] for artist in track_json["artists"]];
        self._lyrics = None;

    def __del__(self) -> None:
        """Destructor to remove cached files."""
        delete_file(self._album_art);

    def _set_lyrics(self, lyric_json: dict[str]) -> None:
        """Sets the lyric member variable."""
        if lyric_json["message"]["header"]["status_code"] == 200:
            raw_lyrics = lyric_json["message"]["body"]["lyrics"]["lyrics_body"];

            # Error check for tracks with no lyrics.
            if not raw_lyrics:
                return;

            # Cut lyrics to remove the MusixMatch text-mark.
            #   6 in this case represents additional \n characters and the "..." substring.
            clip_index = raw_lyrics.index(r"******* This Lyrics is NOT for Commercial use *******") - 6;
            self._lyrics = raw_lyrics[:clip_index];

    def get_lyrics(self) -> str:
        """Returns the lyrics of the track."""
        if self._lyrics:
            return self._lyrics;
        else:
            raise NoLyricsException;

    def get_name(self) -> str:
        """Returns the name of the track."""
        return self._name;

    def get_clean_name(self) -> str:
        """Returns the shortened name of the track, removing any unnecessary text. """
        # Common track extensions for track titles.
        # i.e. "(feat. )"", "- Radio Mix", "- Single Version", "- 20XX Remaster", etc.
        extensions = {'/', '-', '(', ')'}
        for i, char in enumerate(self._name):
            if char in extensions:
                if i > 0 and self._name[i-1] in whitespace:
                    return self._name[:i-1]
                else:
                    return self._name[:i]
        return self._name

    def get_album(self) -> str:
        """Returns the name of the album for the track."""
        return self._album;

    def get_raw_artists(self) -> list[str]:
        """Returns a list of the artists names."""
        return self._artists;

    def get_artists(self) -> str:
        """Returns a concatenated string the artists names."""
        return ", ".join(self._artists);

    def get_album_art(self) -> str:
        """Returns the file path to the album art for the track."""
        return self._album_art;

    def __str__(self) -> str:
        return f"'{self.get_name()}' by {self.get_artists()}";
