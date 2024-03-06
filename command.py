import json
import os

import config

from get_url import get_url
from play_songs import play_songs
from selected_song import refresh_screen
from show_playlist import show_playlist
from footer import footer


class Command:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def main(self, stdscr, user_input, get_input):
        user_input = user_input.replace(" ", "")
        command, list = user_input.split(':', 1)

        if command == 'playlist':
            playlist_path = os.path.join(config.base_dir, 'playlists', f'{list}.json')
            if os.path.exists(playlist_path):
                with open(playlist_path, 'r') as file:
                    title = json.load(file)
                if get_url(title, stdscr):
                    return play_songs(stdscr, get_input)
            else:
                return show_playlist(stdscr, get_input)
        elif command == 'list':
            return show_playlist(stdscr, get_input)
        
    def player(self, string, stdscr, player_input  ):
        string = string.replace(" ", "")
        command, query = string.split(':', 1)
        queries = query.split(',')

        if command == 'add':
            if len(queries) == 0: return
            get_url(queries, stdscr, False)
            player_input.player_input = ''
            
        elif command == 'del':
            if len(config.info_list) == 1: return
            for index , song in enumerate(queries):
                try:
                    if int(song) != config.row:
                        config.info_list.pop(int(song) - 1 - index)
                        if config.row != 1:
                            config.row -= 1
                except:
                    pass
            refresh_screen(stdscr, player_input)
            player_input.player_input = ''

        elif command == 'save':
            playlist_path = os.path.join(config.base_dir, 'playlists', f'{queries[0]}.json')
            if len(query) == 0: return
            title = [item[0] for item in config.info_list]
            with open(playlist_path, 'w') as file:
                json.dump(title, file)
            player_input.player_input = ''

        elif command == 'remove':
            playlist_path = os.path.join(config.base_dir, 'playlists', f'{queries[0]}.json')
            if os.path.exists(playlist_path):
                os.remove(playlist_path)
            player_input.player_input = ''

        else:
            player_input.player_input = ''

        footer.init(stdscr, config.play_description)

    def list(self, string, stdscr, get_input):
        string = string.replace(" ", "")
        command, query = string.split(':', 1)

        if command == 'remove':
            playlist_dir = os.path.join(config.base_dir, 'playlists')
            playlist_files = os.listdir(playlist_dir)
            try:
                file_name = playlist_files[int(query) - 1]
                playlist_path = os.path.join(playlist_dir, file_name)
                if os.path.exists(playlist_path):
                    os.remove(playlist_path)
                return show_playlist(stdscr, get_input)
            except:
                pass
        else:
            return show_playlist(stdscr, get_input)
        
command = Command()