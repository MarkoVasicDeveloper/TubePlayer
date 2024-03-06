import curses

import config

from get_url import get_url
from logo_asci import logoASCI
from play_songs import play_songs
from footer import footer
from command import command
from thread.set_thread import set_thread

def logo_screen (stdscr, get_input):
    curses.flushinp()
    config.player_screen = False

    set_thread(stdscr)
        
    logoASCI.logo(stdscr)

    footer.init(stdscr, config.main_description)

    user_input = get_input.main_input()

    if user_input:
        stdscr.clear()
        stdscr.refresh()

        if ':' in user_input: return command.main(stdscr, user_input, get_input)

        queries = user_input.split(', ')

        if get_url(queries, stdscr):
            play_songs(stdscr, get_input)
        else:
            stdscr.addstr(0, 0, "No URLs found for the given query.")
            stdscr.refresh()
