# lyric_tweeter.py

from config import twitter_api, twitter_access
from lyrics import LyricGetter
from track import NoLyricsException
import string
from tweepy import OAuthHandler, API, Forbidden, models


def make_parseable(text: str) -> str:
    return text.translate(str.maketrans('', '', string.punctuation)).lower();


class LyricTweeter:
    def __init__(self, debug=False):
        # Setup Tweeter API Wrapper
        tweet_auth = OAuthHandler(twitter_api.get_key(), twitter_api.get_secret());
        tweet_auth.set_access_token(twitter_access.get_key(), twitter_access.get_secret());
        self._twitter_client = API(auth=tweet_auth, wait_on_rate_limit=True);

        # Grab bot's screen name and user id
        user = self._twitter_client.verify_credentials();
        self._screen_name = user.screen_name;
        self._user_id = user.id;

        # Initialize LyricGetter for access to Spotify and MusixMatch's APIs
        self._lyric_getter = LyricGetter(debug);

        # Initialize to-be-filled member variables
        self._debug = debug;
        self._track = None;
        self._tweet_id = None;
        self._winning_tweet = None;

    def tweet_random_saved_track(self) -> None:
        """Send a tweet with the lyrics of a randomly track from the authenticated user's saved tracks."""

        # Loop until a valid track is found.
        while self._track == None:
            try:
                track = self._lyric_getter.get_random_saved_track();

                tweet_response = self._twitter_client.update_status(
                    self._cut_text_to_tweet(track.get_lyrics())
                );

                self._tweet_id = tweet_response.id;

                self._track = track;

            # A duplicate tweet currently exists.
            except Forbidden:
                if self._debug:
                    print("DUPLICATE TRACK");

            # Track either has no lyrics or lyrics are not available via MusixMatch
            except NoLyricsException:
                if self._debug:
                    print("NO LYRICS FOR TRACK");

        if self._debug:
            print("TWEET SUCCESSFUL");

        return;

    def check_for_winner(self) -> bool:
        """Checks if a winner is found in the replies of the sent lyric tweet."""
        replies = self._get_replies_to_tweet();

        for reply in replies:
            # Remove bot's screen name (@ tag) from the reply.
            text = reply.text[len(f"@{self._screen_name} "):];

            if self._debug:
                print(f"REPLY: '{reply.text}' by @{reply.author.screen_name}");
            
            text = make_parseable(text);

            # Check for winning conditions:
            #       1) Track title is found in reply OR
            #       2) Artist name is found in reply
            if self._track_title_in_text(text) or self._artists_in_text(text):
                self._winning_tweet = reply;

                if self._debug:
                    print(f"WINNER FOUND: @{reply.author.screen_name}");

                return True;

        return False;

    def announce_winner(self) -> None:
        """Announces the winner of the lyric game with the title, artist, and album art."""
        if not self._winning_tweet:
            return;

        # Upload album art from cache.
        album_art= self._twitter_client.chunked_upload(
            self._track.get_album_art(),
            wait_for_async_finalize=True
        );

        if self._debug:
            print(f"ALBUM MEDIA: {album_art}");

        # Send tweet with title, artist, and album art for the track.
        self._twitter_client.update_status(
            f"Yep @{self._winning_tweet.author.screen_name}! The track is {self._track}",
            in_reply_to_status_id=self._tweet_id,
            media_ids=[album_art.media_id]
        );

        return;

    def _get_replies_to_tweet(self) -> list[models.Status]:
        """Returns the replies to the sent lyric tweet."""
        if not self._tweet_id:
            return None;

        # Collects all "@'s"/tags since the lyric tweet was sent.
        tags_since_tweet = self._twitter_client.search_tweets(
            q=f"@{self._screen_name}",
            since_id=self._tweet_id
        );

        # Filters the tweets for those that are replying to the lyric tweet.
        replies = [t for t in tags_since_tweet if t.in_reply_to_status_id == self._tweet_id];

        # Return the filtered tweets, sorted in order of creation time.
        return sorted(replies, key=(lambda t: t.created_at));

    def _clear_timeline(self) -> None:
        """Resets the bot's account, deleting all tweets and replies."""

        # Collects information on the bot.
        user = self._twitter_client.get_user(
            user_id=self._user_id,
            screen_name=self._screen_name
        );

        tweet_count = user.statuses_count;

        # Loops through to delete all tweets/statuses.
        while tweet_count > 200:
            timeline = user.timeline(count=200);

            for status in timeline:
                status.destroy();

            tweet_count -= 200;

        if tweet_count:
            timeline = user.timeline(count=tweet_count);

            for status in timeline:
                status.destroy();

        return;

    def _track_title_in_text(self, text: str) -> bool:
        """Check if the title of the tweeted track is found in text."""

        # Clean up track name
        track_title = make_parseable(self._track.get_name());
        clean_title = make_parseable(self._track.get_clean_name());

        return (track_title in text) or (clean_title in text);

    def _artists_in_text(self, text: str) -> bool:
        """Check if any of the artists on the tweeted track are found in text."""
        # Clean up artists names
        artists = [make_parseable(a) for a in self._track.get_raw_artists()];

        # Check if any artists are in the text.
        for artist in artists:
            if self._specific_artist_in_text(artist, text):
                return True;

        return False;


    @staticmethod
    def _specific_artist_in_text(artist: str, text: str) -> bool:
        """Checks if a specific artist of the track is in text."""
        if artist in text:
            return True

        # Check for parts of a space-separated name.
        for name in artist.split():
            if name in text:
                return True

        return False



    @staticmethod
    def _cut_text_to_tweet(text: str) -> str:
        """Shortens the length of text to fit the size of a tweet."""
        if len(text) < 275:
            return text + "\n...";
        return text[:275] + "\n...";
