import curses

import config

class Footer:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, stdscr, description):
        stdscr.addstr(config.height - 2, 0, description, curses.color_pair(1))
        stdscr.move(config.height - 1, 0)
        stdscr.clrtoeol()
        stdscr.addstr(config.height - 1, 0, '')
        stdscr.refresh()
    
    def next_line(self, stdscr, description, counter, current_line, user_input):
        stdscr.move(current_line - 1, 0)
        stdscr.clrtoeol()
        stdscr.addstr(current_line - 2, 0, description, curses.color_pair(1))
        stdscr.addstr(current_line, 0, user_input[(counter - 1) * config.width : config.width * counter])
        stdscr.move(config.height - 1, 0)

    def input_line(self, stdscr, counter, user_input):
        stdscr.move(config.height - 1, 0)
        stdscr.clrtoeol()
        try:
            stdscr.addstr(config.height - 1, 0, user_input[counter * config.width : config.width * (counter + 1)])
        except:
            pass
        stdscr.refresh()

footer = Footer()