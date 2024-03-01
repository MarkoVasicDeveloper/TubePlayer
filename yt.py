import argparse
import curses
import os
import signal
import subprocess
import sys

from get_url import get_url
from logo_screen import logo_screen
from play_songs import play_songs
import config

def main(stdscr):
    config.stdscr = stdscr
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    if not os.path.exists('playlists'):
        os.makedirs('playlists')

    parser = argparse.ArgumentParser(description='Download or play YouTube video.')
    parser.add_argument('-q', '--query', type=str, help='Search query for YouTube video')

    args = parser.parse_args()

    if args.query:
        queries = args.query.split(', ')
        
        if get_url(queries, stdscr):
            play_songs(stdscr)
        else:
            stdscr.addstr(0, 0, "No URLs found for the given query.")
            stdscr.refresh()
    else:
        logo_screen(stdscr)

def handle_interrupt(signal, frame):
    sys.exit(0)

def get_active_window_id():
    result = subprocess.run(['xdotool', 'getwindowfocus'], capture_output=True, text=True)
    
    if result.returncode == 0:
        config.terminal_id = result.stdout.strip()
    else:
        return None
    
if __name__ == '__main__':
    get_active_window_id()
    signal.signal(signal.SIGINT, handle_interrupt)
    curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.wrapper(main) 