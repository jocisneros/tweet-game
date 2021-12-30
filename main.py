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
    # Initialize program arguments.
    debug, do_clear, wait_time = False, False, None;
    loop_count, user_control = 1, False;

    # Check command-line arguments.
    for arg in args:
        if arg == "-DEBUG":
            debug = True;
        elif arg == "-CLEAR":
            do_clear = True
        elif arg.startswith("-WT="):
            try:
                wait_time = int(arg[4:]);
                if wait_time <= 0:
                    print("Error: Wait time must be a positive number.");
                    return;
            except ValueError:
                print("Error: Wait time must be provided in the format '-WT=NUM'");
                return;
        elif arg.startswith("-LC="):
            try:
                loop_count = int(arg[4:]);
                if loop_count <= 0:
                    print("Error: Loop count must be a positive number.");
                    return;
            except ValueError:
                print("Error: Loop count must be provided in the format: '-LC=NUM");
                return;
        elif arg == "-U":
            user_control = True;

    if do_clear:
        LyricTweeter()._clear_timeline();

    if user_control:
        print("User Control Mode: Enter 'q' to exit program.")

        while True:
            init_game(LyricTweeter(debug), wait_time=wait_time, debug=debug);
            if input("Run Again?") == "q":
                break;

    else:
        for _ in range(loop_count):
            init_game(LyricTweeter(debug), wait_time=wait_time, debug=debug);

    return;


if __name__ == "__main__":
    main(argv);
