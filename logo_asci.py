import curses

from logo import logo

class LogoASCI:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def logo(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        logo_width = len(max(logo.split('\n'), key=len))
        logo_height = len(logo.split('\n'))
        start_x = (width - logo_width) // 2
        start_y = (height - logo_height) // 8

        for i, line in enumerate(logo.split('\n')):
            stdscr.addstr(start_y + i, start_x, line, curses.color_pair(1))

logoASCI = LogoASCI()