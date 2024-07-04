import subprocess
import config

import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_url(queries, stdscr, loading=True):

    if loading:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Loading...')
        stdscr.refresh()

    for index, query in enumerate(queries):
        command = f'yt-dlp -x --get-title --get-url "ytsearch:{query}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        info = result.stdout.splitlines()
        try:
            config.info_list.append((info[0], info[1]))
        except:
            logging.debug(f'Get url: error={result.stdout}')
            
        if loading: stdscr.addstr(0, 0, f'Loading...    {index + 1}/{len(queries)}')
        stdscr.refresh()

    stdscr.clear()

    for index, info in enumerate(config.info_list):
        try:
            stdscr.addstr(index, 0, f'{index + 1}. {info[0]}')
        except:
            pass
        
    stdscr.refresh()

    return True if len(config.info_list) > 0 else False