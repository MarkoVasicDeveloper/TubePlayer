import curses
import os
import signal
import sys

from logo_screen import logo_screen
from user_input import UserInput
from utils import get_active_window_id
import config


def main(stdscr):
    height, width = stdscr.getmaxyx()
    config.stdscr = stdscr
    config.height = height
    config.width = width
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    get_input = UserInput(stdscr)

    if not os.path.exists('playlists'):
        os.makedirs('playlists')

    logo_screen(stdscr, get_input)

def handle_interrupt(_, __):
    sys.exit(0)
    
if __name__ == '__main__':
    get_active_window_id()
    signal.signal(signal.SIGINT, handle_interrupt)
    curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.wrapper(main) 