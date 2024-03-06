import curses
from format_time import format_time
import config
from footer import footer

def play_songs(stdscr, get_input):
    from logo_screen import logo_screen
    config.loop = True
    config.player_screen = True
    curses.flushinp()
    get_input.player_input = ''

    footer.init(stdscr, config.play_description)

    while config.row < len(config.info_list) and config.loop:
        _ , url = config.info_list[config.row]
        config.player.play(url)

        config.row += 1

        config.player.wait_for_playback()

        if config.row == len(config.info_list): config.row = 0

    logo_screen(stdscr, get_input)

def update_progress(stdscr, name, value):
    duration = config.player._get_property('duration')
    time_pos = config.player._get_property('time-pos')
    current_row = config.row + 1 if config.row <= 0 else config.row

    if name == 'percent-pos' and value and time_pos and duration:
        time_pos_str = format_time(time_pos)
        duration_str = format_time(duration)
        progress = int(value)

        info = config.info_list[current_row - 1][0] if current_row - 1 < len(config.info_list) else '' 
        stdscr.addstr(current_row - 1, 0, f'{config.row}. {info} {duration_str} / {time_pos_str}    {progress}%', curses.color_pair(2))
        
        if progress >= 99:
            stdscr.move(current_row - 1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(current_row - 1, 0, f'{current_row}. {config.info_list[current_row - 1][0]}')
            stdscr.refresh()

        stdscr.refresh()