import curses
import sys

from footer import footer
import config


class UserInput:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.user_input = ''
        self.counter = 0
        self.height, self.width = stdscr.getmaxyx()
        self.current_line = self.height - 1
        
    def main_input(self):
        self.user_input = ''
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_ENTER or ch == 10 :
                if(self.user_input.strip() == 'q'): sys.exit()
                if(len(self.user_input) > 0): return self.user_input
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if(len(self.user_input) > 0): self.user_input = self.user_input[:-1]
            elif chr(ch).isalnum() or ch == ord('-') or ch == ord('+') or ch == ord(' ')or ch == ord(',') or ch == ord('.') or ch == ord(':'):
                self.user_input += chr(ch)

            if(len(self.user_input) %  self.width == 0 and len(self.user_input) > 0): 
                self.current_line -= 1
                self.counter += 1

                footer.next_line(self.stdscr, config.main_description, self.counter, self.current_line, self.user_input)

            footer.input_line(self.stdscr, self.counter, self.user_input)

    def list_input(self):
        self.user_input = ''
        while True:
            ch = self.stdscr.getch()
            if ch == 27: return -1

            elif chr(ch).isdigit():
                self.user_input += chr(ch)
            elif ch == curses.KEY_ENTER or ch == 10:
                if self.user_input == '': pass
                if self.user_input != '': return self.user_input
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if(len(self.user_input) > 0): self.user_input = self.user_input[:-1]

            footer.input_line(self.stdscr, self.counter, self.user_input)