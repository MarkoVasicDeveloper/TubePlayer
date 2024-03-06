import threading
import config
from thread.focus import Focus
from thread.player_control import PlayerControl
from thread.player_input import PlayerInput

def set_thread(stdscr):
    if config.terminal_id is not None and config.focus_thread is None:
        focus = Focus(config)
        focus_thread = threading.Thread(target=focus.start, daemon=True)
        focus_thread.start()
        config.focus_thread = True

    if config.input_thread is None:
        player_input = PlayerInput(stdscr)
        player_input_thread = threading.Thread(target=player_input.start, daemon=True)
        player_input_thread.start()

        player = PlayerControl(stdscr, config, player_input)
        control_input_thread = threading.Thread(target=player.start, daemon=True)
        control_input_thread.start()
        config.input_thread = True