import curses
import json
import os

import config
import sys
import threading

from get_url import get_url
from keyboard_handlers import focus_listener, player_user_input_listener, start_listener
from play_songs import play_songs
from logo import logo

def logo_screen (stdscr):
    curses.flushinp()
    if config.terminal_id is not None and config.focus_thread is None:
        focus_thread = threading.Thread(target=focus_listener, daemon=True)
        focus_thread.start()
        config.focus_thread = True
    
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    logo_width = len(max(logo.split('\n'), key=len))
    logo_height = len(logo.split('\n'))
    start_x = (width - logo_width) // 2
    start_y = (height - logo_height) // 8

    for i, line in enumerate(logo.split('\n')):
        stdscr.addstr(start_y + i, start_x, line, curses.color_pair(1))

    user_input = ''
    current_line = height - 1
    counter = 0

    stdscr.addstr(current_line - 2, 0, "Queries separate by , / playlist:  list name / list: show all playlist / q for quit", curses.color_pair(1))
    stdscr.move(current_line, 0)
    stdscr.clrtoeol()
    stdscr.addstr(height - 1, 0, user_input)
    stdscr.refresh()

    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_ENTER or ch == 10 :
            if(user_input.strip() == 'q'): sys.exit()
            if(len(user_input) > 0): break
        elif ch == curses.KEY_BACKSPACE or ch == 127:
            if(len(user_input) > 0): user_input = user_input[:-1]
        elif chr(ch).isalnum() or ch == ord('-') or ch == ord('+') or ch == ord(' ')or ch == ord(',') or ch == ord('.') or ch == ord(':'):
            user_input += chr(ch)

        if(len(user_input) %  width == 0 and len(user_input) > 0): 
            current_line -= 1
            counter += 1
            
            stdscr.move(current_line - 1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(current_line - 2, 0, "Queries separate by , / playlist:  list name / list: show all playlist / q for quit", curses.color_pair(1))
            stdscr.addstr(current_line, 0, user_input[(counter - 1) * width : width * counter])
            stdscr.move(height - 1, 0)


        stdscr.clrtoeol()
        try:
            stdscr.addstr(height - 1, 0, user_input[counter * width : width * (counter + 1)])
        except:
            pass
        stdscr.refresh()

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
                        return play_songs(stdscr)
            elif command == 'list':
                return show_playlist(stdscr)

        queries = user_input.split(', ')

        if get_url(queries, stdscr):
            user_input = ''
            play_songs(stdscr)
        else:
            stdscr.addstr(0, 0, "No URLs found for the given query.")
            stdscr.refresh()

def show_playlist(stdscr):
    height, _ = stdscr.getmaxyx()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    playlist_dir = os.path.join(base_dir, 'playlists')

    playlist_files = os.listdir(playlist_dir)

    if len(playlist_files) == 0:
        stdscr.clear()
        stdscr.addstr(0, 0, 'No playlists')
    
    stdscr.clear()
    for index, file_name in enumerate(playlist_files):
        file_name_without_extension = os.path.splitext(file_name)[0]
        try:
            stdscr.addstr(index, 0, f'{index + 1}. {file_name_without_extension}')
        except:
            pass

    stdscr.move(height - 1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(height - 2, 0, "Enter list number  / remove: list number / ESC to return ")
    stdscr.move(height - 1, 0)

    user_input = ''
    while True:
        ch = stdscr.getch()
        if ch == 27:
            logo_screen(stdscr)
        elif chr(ch).isdigit():
            user_input += chr(ch)
        elif ch == curses.KEY_ENTER:
            if user_input == '': return
            index = int(user_input) - 1
            if index < len(playlist_files):
                file_name = playlist_files[index]
                playlist_path = os.path.join(playlist_dir, file_name)
                if os.path.exists(playlist_path):
                    with open(playlist_path, 'r') as file:
                        title = json.load(file)
                    if get_url(title, stdscr):
                        return play_songs(stdscr)
        elif ch == curses.KEY_BACKSPACE or ch == 127:
            if(len(user_input) > 0): user_input = user_input[:-1]
                    
        stdscr.clrtoeol()
        stdscr.addstr(height -1, 0, user_input)
        stdscr.refresh()
