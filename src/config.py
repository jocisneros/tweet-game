# config.py

from api_credentials import APICredentials

twitter_api = APICredentials(
	key=r"<YOUR TWITTER API KEY>",
	secret=r"<YOUR TWITTER API SECRET>"
);

twitter_access = APICredentials(
	key=r"<YOUR TWITTER ACCESS TOKEN>",
	secret=r"<YOUR TWITTER ACCESS SECRET>",
	bearer=r"<YOUR TWITTER BEARER TOKEN>"
);

spotify = APICredentials(
	key=r"<YOUR SPOTIFY CLIENT ID>",
	secret=r"<YOUR SPOTIFY CLIENT>"
);

musix_match = APICredentials(
	key=r"<YOUR MUSIXMATCH API KEY>"
);
