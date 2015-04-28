#last2gmb

This is an inefficient and ugly script which attempts to sync your playcounts exported from last.fm with your gmusicbrowser library playcounts. It uses the pandas library for grouping scrobbles and querying the gmb library. Enjoy.
Please note: this code is still under development, has not been properly tested, and may not work. Make sure to back up your gmb library.

##Features

- works offline and takes about half an hour to complete with a ~60k song library with ~100k scrobbles (sluggish, I know)
- uses your original metadata at the time of scrobbling a song and tries to find it in your gmb library, so it should work for all the songs where the metadata (artist, song name, album) were not edited in between scrobbling and running this
- backs up your original gmbrc library file before overwriting it

##Installation

- clone the repo
- install the libraries from the requirements.txt, preferably in a virtualenv with pip

##Usage 

**!!!Remember to close gmusicbrowser before running the script!!!**

1. go to your last.fm settings -> export data tab -> request your last.fm archive (it should arrive by email in a few days)
2. decompress the file and locate the scrobbles.tsv file
3. cd to the src folder and run this in terminal, adjusted to your file paths for gmbrc and scrobbles.tsv

        ```shell
   
        python main.py --gmbrc /home/USER/.config/gmusicbrowser/gmbrc --lastdb /PATH/TO/scrobbles.tsv
        
        ```

4. if you wish to revert for any reason, a backup file named gmbrc_backup_timestring should be in the gmusicbrowser folder

##Todo

- try to match actual artist name and song title if uncorrected_artist_name and uncorrected_song_title fail to match
- add proper support for utf8 strings
- match artist collaborations (gmb splits them as separate artists)
- dump log of unmatched entries (maybe just albums) to a file instead of stdout
- some kind of terminal progress bar and ETA
- optimize literally everything