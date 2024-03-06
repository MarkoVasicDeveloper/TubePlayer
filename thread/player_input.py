from pynput.keyboard import Key, Listener
from footer import footer
from command import command
import config

class PlayerInput:
    def __init__(self, stdscr) -> None:
        self.player_input = ''
        self.stdscr = stdscr
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        if config.player_screen and config.focus_thread:
            if hasattr(key, 'char'):
                try:
                    self.player_input += key.char
                except:
                    pass
                
            elif key == Key.space: self.player_input += ' '
                
            elif key == Key.backspace:
                if(len(self.player_input) > 0): self.player_input = self.player_input[:-1]

            elif key == Key.enter and self.player_input > '':
                if ':' in self.player_input : command.player(self.player_input, self.stdscr, self )
                self.player_input = ''

            footer.input_line(self.stdscr, 0, self.player_input)

    def start(self):
        self.listener.join()