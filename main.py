# main.py

from src.lyric_tweeter import LyricTweeter
from sys import argv
from time import sleep


def init_game(tweeter: LyricTweeter, wait_time: int, debug=False) -> None:
    """Initialize Lyric Tweet Game."""
    tweeter.tweet_random_saved_track();
    sleep(wait_time);

    while not tweeter.check_for_winner():
        if debug:
            print("NO WINNER FOUND THIS LOOP")
        sleep(wait_time)

    tweeter.announce_winner();
    return;


def main(args: list[str]) -> None:
    # Initialize program arguments
    debug, do_clear, wait_time = False, False, None;

    for arg in args:
        if arg == "-DEBUG":
            debug = True;
        elif arg == "-CLEAR":
            do_clear = True
        elif arg.startswith("-WT="):
            try:
                wait_time = int(arg[4:]);
                if wait_time <= 0:
                    print("Error: Wait time must be a positive number.")
                    return;
            except ValueError:
                print("Error: Wait time must be provided in the format '-WT=<integer>'");
                return;

    lyric_tweeter = LyricTweeter(debug);

    if do_clear:
        lyric_tweeter._clear_timeline();

    init_game(lyric_tweeter, wait_time=wait_time, debug=debug);
    return;


if __name__ == "__main__":
    while 1:
        main(argv)
        i = input("NEXT GAME?")
        if i == 'q':
            break;
