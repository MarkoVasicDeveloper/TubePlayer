import os
import mpv

from play_songs import update_progress

stdscr = None

info_list = []
terminal_id = None

main_description = "Queries separate by , / playlist:  list name / list: show all playlist / q for quit"
list_description = "Enter list number  / remove: list number / ESC to return "
play_description = 'add: queries / del: number / separate by , / save: or remove: list / ESC to return'

base_dir = os.path.dirname(os.path.abspath(__file__))

height = None
width = None

row = 0
selected_row = 0
input_thread = None
focus_thread = None
player_screen = False
loop = True

player = mpv.MPV(input_default_bindings=True)
player.observe_property('percent-pos', lambda name, value: update_progress(stdscr, name, value))