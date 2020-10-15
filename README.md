# Speedrun.com Backup
Simple script to download a backup of all raw data of one or more games on [Speedrun.com](https://speedrun.com). The downloaded data consists of raw json files with all runs and game information needed to set up a leaderboard.

The script does no processing whatsoever, but with a little programming knowledge you can easily convert the files into a database format. This script just provides a quick way to make sure you have all the leaderboard data of your speedgame at hand.

## Usage
* Open the script `backup.py` in a text editor and replace the list in `GAMES = []` on line 7 with a list of the abbreviations of the games you would like to backup, for example `GAMES = ['sm64'. 'smo']`.
* Run the script with `python backup.py`. You may have to install the requests module first (`pip install requests`). The script should start downloading all the data. For big games, this may take up to a few minutes.

## Output
The script outputs two text files per game, which will be saved in the root directory with a timestamp and the game abbreviation:
* `[timestamp]_[game]_game_data.txt` has three entries:
  * **'game'** contains general data on the game, mainly the moderators, regions and platforms it has.
  * **'categories'** lists all the categories and subcategories ('variables'), and their rules. Also includes the individual level categories.
  * **'levels'** lists all the individual levels and their rules.
* `[timestamp]_[game]_runs.txt` consists of ALL submitted runs of the game, sorted by submit date (most recent first). This includes all categories and subcategories, individual levels, obsolete runs and rejected runs. Values like the category name, variable names, the examiner, the region and the platform are saved as an id string. The game_data.txt file can be used to look up the normal names for these entities.

Note that the main game rules (when you click 'main rules' when viewing any rules) are not included! They were added later to SRC and I haven't found a way to retrieve them through the API, so if you want to back those up make sure to save them manually.
