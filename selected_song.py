import curses
import config

def selected_song(stdscr):
    height, _ = stdscr.getmaxyx()
    stdscr.clear()

    for i, (title, _) in enumerate(config.info_list):
        if i == config.selected_row:
            stdscr.addstr(f'{i + 1}. {title}', curses.color_pair(1))
        else:
            stdscr.addstr(f'{i + 1}. {title}')
        stdscr.addstr('\n')

    stdscr.addstr(height - 2, 0, 'add: queries / del: number / separate by , / save: or remove: list', curses.color_pair(1))
    stdscr.move(height - 1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(height - 1, 0, config.player_screen_user_input)
    stdscr.refresh()

def refresh_screen(stdscr):
    height, width = stdscr.getmaxyx()
    stdscr.clear()
    for i, (title, _) in enumerate(config.info_list):
        stdscr.addstr(f'{i + 1}. {title}')
        stdscr.addstr('\n')

    stdscr.addstr(height - 2, 0, 'add: queries / del: number / separate by , / save: or remove: list', curses.color_pair(1))
    stdscr.move(height - 1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(height - 1, 0, config.player_screen_user_input)
    stdscr.refresh()