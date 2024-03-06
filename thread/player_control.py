from pynput.keyboard import Key, Listener

from selected_song import refresh_screen, selected_song

class PlayerControl:
    def __init__(self, stdscr, config, player_input) -> None:
        self.player_input = player_input
        self.stdscr = stdscr
        self.config = config
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        if self.config.player_screen and self.config.focus_thread:
            if key == Key.left: self.seek_player(-5)
            elif key == Key.right: self.seek_player(5)
            elif key == Key.esc: self.stop_player()
            elif key == Key.up: self.move_selected_song(-1)
            elif key == Key.down: self.move_selected_song(1)
            elif key == Key.enter and self.player_input.player_input == '': self.handle_enter()

    def start(self):
        self.listener.join()

    def seek_player(self, seconds):
        try:
            self.config.player.seek(seconds)
        except:
            pass

    def stop_player(self):
        duration = self.config.player.duration
        if duration is not None:
            self.config.player.seek(duration)
        self.config.player.stop(keep_playlist=False)
        self.config.loop = False
        self.config.info_list = []
        self.config.row = 0
        self.config.selected_row = 0
        self.player_input.player_input = ''

    def move_selected_song(self, direction):
        if 0 <= self.config.selected_row + direction < len(self.config.info_list):
            self.config.selected_row += direction
            selected_song(self.stdscr, self.player_input)

    def handle_enter(self):
        duration = self.config.player.duration
        if duration is not None:
            self.config.row = self.config.selected_row
            self.config.player.seek(duration)
            refresh_screen(self.stdscr, self.player_input)