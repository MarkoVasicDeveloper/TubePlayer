from pynput.keyboard import Listener
import ewmh

class Focus:
    def __init__(self, config) -> None:
        self.config = config
        self.listener = Listener(on_press=self.on_focus)
        self.listener.start()

    def on_focus(self, _):
        ewmh_objekat = ewmh.EWMH()
        focused_window = ewmh_objekat.getActiveWindow()

        if int(self.config.terminal_id) == int(focused_window.id):
            self.config.focus_thread = True
        else:
            self.config.focus_thread = False

    def start(self):
        self.listener.join()