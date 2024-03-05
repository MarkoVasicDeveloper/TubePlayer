import curses
import config
from footer import footer

def selected_song(stdscr):
    stdscr.clear()

    for i, (title, _) in enumerate(config.info_list):
        if i == config.selected_row:
            stdscr.addstr(f'{i + 1}. {title}', curses.color_pair(1))
        else:
            stdscr.addstr(f'{i + 1}. {title}')
        stdscr.addstr('\n')

    footer.init(stdscr, config.play_description)
    footer.input_line(stdscr, 0, config.player_screen_user_input)

def refresh_screen(stdscr):
    stdscr.clear()
    for i, (title, _) in enumerate(config.info_list):
        stdscr.addstr(f'{i + 1}. {title}')
        stdscr.addstr('\n')

    footer.init(stdscr, config.play_description)
    footer.input_line(stdscr, 0, config.player_screen_user_input)