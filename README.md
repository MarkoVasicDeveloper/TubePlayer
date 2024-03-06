# TubePlayer

### Audio player for youtube

#### Installation

```bash
git clone https://github.com/MarkoVasicDeveloper/TubePlayer.git
pip install -r requirements.txt
cd TubePlayer
python3 yt.py
```

### Usage

#### Main screen

Now, you are on the main screen. You can type song or array of songs separated by commas and press enter. The script will find all songs and takes you to the player screen.

##### Main screen commands

- **playlist:** <br>

    >If you have a saved list, use this command to load your list.
- **list**: <br>

    >This command will move you to the list screen, where you can manipulate your playlist.
- **q**: <br>

    >For quitting the script.

> **Notice:**   All commands have to end with colon

##### Player screen commands

- **add**: <br>

    >Use this command to add song or array of songs separate by comma. This command will add song/s to current player, not in your playlist.
- **del**: <br>

    >Delete the song specified by number.

- **save**: <br>

    >This command will save songs in playlist. After command, type name of playlist.

- **remove**: <br>

    >This command will delete the playlist.

- **ESC** <br>

    >Pressing ESC will return you to the main screen.
> **Notice:**   All commands have to end with colon

##### List screen commands

On this screen, you will see all of your lists.

- **list number** <br>

    >Simply type list number and press Enter to load the playlist.

- **remove:** <br>

    >This command will remove playlist at that number.

- **ESC** <br>

    >Press ESC to return to the main screen

> **Notice:**   All commands have to end with colon