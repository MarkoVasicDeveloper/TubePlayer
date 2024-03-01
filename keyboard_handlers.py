import sys
from pynput.keyboard import Key, Listener

from selected_song import refresh_screen, selected_song
import config

if sys.platform == 'linux':
    import ewmh
elif sys.platform == 'win32':
    import pygetwindow as gw

def on_press(stdscr, key):

    if config.player_screen and config.focus_thread:
        if key == Key.left:
            config.player.seek(-5)
        elif key == Key.right:
            config.player.seek(5)
        elif key == Key.esc:
            duration = config.player.duration
            if duration is not None:
                config.player.seek(duration)
            config.player.stop(keep_playlist=False)
            config.loop = False
            config.info_list = []
            config.row = 0
            config.selected_row = 0
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
    height, _ = stdscr.getmaxyx()

    if config.player_screen and config.focus_thread:
        if hasattr(key, 'char'):
            config.player_screen_user_input += key.char
            stdscr.clrtoeol()
            stdscr.addstr(height - 1, 0, config.player_screen_user_input)
            stdscr.refresh()
        elif key == Key.space:
            config.player_screen_user_input += ' '
            stdscr.clrtoeol()
            stdscr.addstr(height - 1, 0, config.player_screen_user_input)
            stdscr.refresh()
        elif key == Key.backspace:
            if(len(config.player_screen_user_input) > 0):
                config.player_screen_user_input = config.player_screen_user_input[:-1]
            stdscr.move(height - 1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(height - 1, 0, config.player_screen_user_input)
            stdscr.refresh()

def player_user_input_listener(stdscr):
    with Listener(on_press=lambda key: player_user_input(stdscr, key)) as listener:
        listener.join()