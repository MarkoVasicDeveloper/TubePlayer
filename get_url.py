import subprocess
import config

def get_url(queries, stdscr):
    stdscr.addstr(0, 0, 'Loading...')
    stdscr.refresh()

    for index, query in enumerate(queries):
        command = f'yt-dlp -x --get-title --get-url "ytsearch:{query}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        info = result.stdout.splitlines()
        config.info_list.append((info[0], info[1]))
        stdscr.addstr(0, 0, f'Loading...    {index + 1}/{len(queries)}')
        stdscr.refresh()

    for index, info in enumerate(config.info_list):
        stdscr.addstr(index, 0, f'{index + 1}. {info[0]}')
        
    stdscr.refresh()

    return True if len(config.info_list) > 0 else False