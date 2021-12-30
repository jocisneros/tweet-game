# lyrics.py

from config import musix_match, spotify
from musixmatch import Musixmatch
from random import randrange
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from track import Track


class LyricGetter:
    def __init__(self, debug=False):
        self._debug = debug;

        # Setup MusixMatch and Spotify API wrappers

        self._musixmatch = Musixmatch(musix_match.get_key());
        self._spotify = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=spotify.get_key(),
                client_secret=spotify.get_secret(),
                redirect_uri="http://localhost:8080",
                scope="user-library-read"
            )
        );

    def get_random_saved_track(self) -> Track:
        """Returns a random track from the authenticated user's saved tracks."""

        # Use the first API call to determine the number of saved tracks
        num_saved_tracks = int(self._spotify.current_user_saved_tracks(limit=1)["total"]);

        # Using the number of saved tracks, call the Spotify API to return a single track
        # offset by the randomly generated number from 0 to the number of saved tracks - 1
        spot_response = self._spotify.current_user_saved_tracks(
            limit=1,
            offset=randrange(0, num_saved_tracks - 1)
        );

        if self._debug:
            print(f"SPOTIFY TRACK GET RESPONSE: {spot_response}")

        # Create the track object and store the lyrics
        track = Track(
            track_json=spot_response["items"][0]["track"],
            added_date=spot_response["items"][0]
        );

        mm_response = self._musixmatch.matcher_lyrics_get(
            track.get_clean_name(),
            track.get_artists()
        )

        if self._debug:
            print(f"SPOTIFY TRACK: {track}");
            print(f"MUSIX MATCH LYRIC LOOKUP RESPONSE: {mm_response}");

        track._set_lyrics(mm_response);
        return track


if __name__ == "__main__":
    lyrics = LyricGetter(True)
    for _ in range(1):
        track = lyrics.get_random_saved_track();
        print(f"{track}\n{track.get_lyrics()}\n")
