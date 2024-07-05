from pynput.keyboard import Listener

from utils import get_active_window_id


class Focus:
    def __init__(self, config) -> None:
        self.config = config
        self.listener = Listener(on_press=self.on_focus)
        self.listener.start()

    def on_focus(self, _):
        focused_window_id = get_active_window_id()

        if self.config.terminal_id == focused_window_id:
            self.config.focus_thread = True
        else:
            self.config.focus_thread = False

    def start(self):
        self.listener.join()