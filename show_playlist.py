import json
import os

import config

from footer import footer
from get_url import get_url
from play_songs import play_songs

def show_playlist(stdscr, get_input):
    from logo_screen import logo_screen
    playlist_dir = os.path.join(config.base_dir, 'playlists')

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
    user_input = get_input.list_input()
 
    if user_input == -1: return logo_screen(stdscr, get_input)
    index = int(user_input) - 1
    if index < len(playlist_files):
        file_name = playlist_files[index]
        playlist_path = os.path.join(playlist_dir, file_name)
        if os.path.exists(playlist_path):
            with open(playlist_path, 'r') as file:
                title = json.load(file)
            if get_url(title, stdscr):
                return play_songs(stdscr)