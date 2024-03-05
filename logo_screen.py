import curses
import json
import os

import config
import sys
import threading

from get_url import get_url
from keyboard_handlers import focus_listener, player_user_input_listener, start_listener
from logo_asci import logoASCI
from play_songs import play_songs

from footer import footer

def logo_screen (stdscr, input):
    curses.flushinp()
    if config.terminal_id is not None and config.focus_thread is None:
        focus_thread = threading.Thread(target=focus_listener, daemon=True)
        focus_thread.start()
        config.focus_thread = True
    config.player_screen = False
        
    logoASCI.logo(stdscr)

    footer.init(stdscr, config.main_description)

    user_input = input.main_input()

    if user_input:
        stdscr.clear()
        stdscr.refresh()

        if config.listener_thread is None:
            listener_thread = threading.Thread(target=start_listener, args=(stdscr,), daemon=True)
            listener_thread.start()
            config.listener_thread = True

        if config.player_user_input_thread is None:
            player_user_input_thread = threading.Thread(target=player_user_input_listener, args=(stdscr,), daemon=True)
            player_user_input_thread.start()
            config.player_user_input_thread = True

        if ':' in user_input:
            user_input = user_input.replace(" ", "")
            command, list = user_input.split(':', 1)
            if command == 'playlist':
                base_dir = os.path.dirname(os.path.abspath(__file__))
                playlist_path = os.path.join(base_dir, 'playlists', f'{list}.json')
                if os.path.exists(playlist_path):
                    with open(playlist_path, 'r') as file:
                        title = json.load(file)
                    if get_url(title, stdscr):
                        return play_songs(stdscr, input)
            elif command == 'list':
                return show_playlist(stdscr, input)

        queries = user_input.split(', ')

        if get_url(queries, stdscr):
            user_input = ''
            play_songs(stdscr, input)
        else:
            stdscr.addstr(0, 0, "No URLs found for the given query.")
            stdscr.refresh()

def show_playlist(stdscr, input):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    playlist_dir = os.path.join(base_dir, 'playlists')

    playlist_files = os.listdir(playlist_dir)

    stdscr.clear()

    if len(playlist_files) == 0:
        stdscr.clear()
        stdscr.addstr(0, 0, 'No playlists')
    else:
        for index, file_name in enumerate(playlist_files):
            file_name_without_extension = os.path.splitext(file_name)[0]
            try:
                stdscr.addstr(index, 0, f'{index + 1}. {file_name_without_extension}')
            except:
                pass

    footer.init(stdscr, config.list_description)

    user_input = input.list_input()
 
    if user_input == -1: return logo_screen(stdscr, input)
    index = int(user_input) - 1
    if index < len(playlist_files):
        file_name = playlist_files[index]
        playlist_path = os.path.join(playlist_dir, file_name)
        if os.path.exists(playlist_path):
            with open(playlist_path, 'r') as file:
                title = json.load(file)
            if get_url(title, stdscr):
                return play_songs(stdscr)
