# Tweet Game
A Twitter program developed with Python 3.10.

This program allows user's to link their Spotify accounts with a Twitter developer account to tweet a small portion of lyrics from a randomly selected track from the user's saved tracks on Spotify.

If a user correctly guesses the song and/or artist(s) of the track based on only tweeted lyrics, the program with announce the winner by tagging them (@'ing) and provide the name, artist(s) names, and album art of the track.

Working example can be found [here](https://twitter.com/jozayeBot)

## Instructions on how to run the program.

### Setup Developer Accounts:

#### Spotify

Login or create an account [here](https://developer.spotify.com/dashboard/login).

1. Create an App.
2. Fill in the App Name and Description.
3. Review and Accept Spotify's Developer Terms of Service and Branding Guidelines.
4. Edit Settings.
5. Set the Redirect URI to http://localhost:8080
6. Store the Client ID and Client Secret.

#### MusixMatch

Login or create an account [here](https://developer.musixmatch.com/signup).

1. Go [here](https://developer.musixmatch.com/) and click "Get Started"
2. Under "Free" click "GET STARTED".
3. Go to Account > Dashboard > Applications.
4. Store the API Key next to your app's name.

#### Twitter

Login or create an account [here](https://developer.twitter.com/).

### Write Keys to File

Using the keys, secrets, and bearer collected from the different dev accounts, copy the data in the respective variables in **src/config.py**

### Run:

`pip install -r requirements.txt`

`python main.py [OPTION...]`
    
##### OPTIONS:
    
    -DEBUG: Outputs debugging information (api responses, state changes, etc.)
    -CLEAR: Clears the timeline of the bot, removing all tweets and replies.
    -WT=NUM: Defines the time to wait when checking for replies to the lyric tweet.
    -U: Actives User Control Mode, allowing the user to control the number of times the program runs.
    -LC=NUM: Defines the number of times the program should run.

