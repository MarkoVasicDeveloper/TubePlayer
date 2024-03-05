import curses

import config
import threading

from get_url import get_url
from keyboard_handlers import focus_listener, player_user_input_listener, start_listener
from logo_asci import logoASCI
from play_songs import play_songs

from footer import footer
from command import command
from player_control import PlayerControl

def logo_screen (stdscr, get_input):
    curses.flushinp()
    if config.terminal_id is not None and config.focus_thread is None:
        focus_thread = threading.Thread(target=focus_listener, daemon=True)
        focus_thread.start()
        config.focus_thread = True
    config.player_screen = False
        
    logoASCI.logo(stdscr)

    footer.init(stdscr, config.main_description)

    user_input = get_input.main_input()

    if user_input:
        stdscr.clear()
        stdscr.refresh()

        if config.listener_thread is None:
            listener_thread = threading.Thread(target=start_listener, args=(stdscr,), daemon=True)
            listener_thread.start()
            config.listener_thread = True

        if config.player_user_input_thread is None:
            player = PlayerControl(stdscr, config)
            player_user_input_thread = threading.Thread(target=player.start,)
            player_user_input_thread.start()
            config.player_user_input_thread = True

        if ':' in user_input:return command.main(stdscr, user_input, get_input)

        queries = user_input.split(', ')

        if get_url(queries, stdscr):
            play_songs(stdscr, get_input)
        else:
            stdscr.addstr(0, 0, "No URLs found for the given query.")
            stdscr.refresh()
