import curses
import os
import sys
from pynput.keyboard import Key, Listener
from get_url import get_url
import json

from selected_song import refresh_screen, selected_song
from command import command
from footer import footer
import config

if sys.platform == 'linux':
    import ewmh
elif sys.platform == 'win32':
    import pygetwindow as gw

def on_press(stdscr, key):

    if config.player_screen and config.focus_thread:
        if key == Key.left:
            try:
                config.player.seek(-5)
            except:
                pass
        elif key == Key.right:
            try:
                config.player.seek(5)
            except:
                pass
        elif key == Key.esc:
            duration = config.player.duration
            if duration is not None:
                config.player.seek(duration)
            config.player.stop(keep_playlist=False)
            config.loop = False
            config.info_list = []
            config.row = 0
            config.selected_row = 0
            config.player_screen_user_input == ''
        elif key == Key.up:
            if config.selected_row >= 1: 
                config.selected_row -= 1
                selected_song(stdscr)
        elif key == Key.down:
            if config.selected_row < len(config.info_list) - 1:
                config.selected_row += 1
                selected_song(stdscr)
        elif key == Key.enter and config.player_screen_user_input == '': 
            duration = config.player.duration
            if duration is not None:
                config.row = config.selected_row
                config.player.seek(duration)
                refresh_screen(stdscr)

def start_listener(stdscr):
    with Listener(on_press=lambda key: on_press(stdscr, key)) as listener:
        listener.join()

def on_focus():
    ewmh_objekat = ewmh.EWMH()
    focused_window = ewmh_objekat.getActiveWindow()

    if int(config.terminal_id) == int(focused_window.id):
        config.focus_thread = True
    else:
        config.focus_thread = False

def focus_listener():
    with Listener(on_press=lambda _: on_focus()) as listener:
        listener.join()

def player_user_input(stdscr, key):

    if config.player_screen and config.focus_thread:
        if hasattr(key, 'char'):
            try:
                config.player_screen_user_input += key.char
            except:
                pass
            
        elif key == Key.space:
            config.player_screen_user_input += ' '
            
        elif key == Key.backspace:
            if(len(config.player_screen_user_input) > 0):
                config.player_screen_user_input = config.player_screen_user_input[:-1]

        elif key == Key.enter and config.player_screen_user_input > '':
            command.player(config.player_screen_user_input, stdscr)

        footer.input_line(stdscr, 0, config.player_screen_user_input)

def player_user_input_listener(stdscr):
    with Listener(on_press=lambda key: player_user_input(stdscr, key)) as listener:
        listener.join()