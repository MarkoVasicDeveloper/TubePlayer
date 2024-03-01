import mpv

from play_songs import update_progress

stdscr = None

info_list = []
terminal_id = None

player_screen_user_input = ''

row = 0
selected_row = 0
listener_thread = None
focus_thread = None
player_user_input_thread = None
player_screen = False
loop = True

player = mpv.MPV(input_default_bindings=True)
player.observe_property('percent-pos', lambda name, value: update_progress(stdscr, name, value))