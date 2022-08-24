External Dependencies:
Cursor
Pyperclip (Optional and can be disabled in the startup() configuration)
Pynput
SpotiPy
Flask
win32gui
win32con

Important Information:
For now, settings.txt will not auto-create if it doesn't exist. This file is used to store the API Token
when the program is not in use. DO NOT delete this file, if you do you will encounter an error.

Instructions for use:
For first time setup, run the "Token Updater" shortcut from the root folder.
It should ask for spotify authorization. This is just the authorization code flow for OAuth that we use to get a token.
once the flask terminal says something along the lines of /refreshtoken 200 in green, you should be set.
Launch the "Main Program" shortcut from the root folder.

Functions (WIP)
get_api_information()
this function gets API information from the spotify API using the requests module. once it gets information,
it saves the information it recieved in json_resp to be used later in the function after errorfinder() has run.
after errorfinder() is done, it will save all the information in correct format to a dictionary which is used in main()

main()
After everything else has ran, main() takes all the information from current_api_info (dict), and prints it on screen.

errorfinder()
This function searches for errors or invalid information in json_resp.
If/when it finds errors, it will let you know and attempt to handle them.

tokenrefresher()
This function is not entirely complete. It will attempt to refresh the token without user input, but it is not tested yet.
If it fails to do so, just close the program, run the token refresher manually, and restart the program.
cmdflask.py is still included, because this is a known reliable method, and is what Token Refresher uses.

Startup():
This function sets all initial configuration variables so they can be used later.
It retrieves an access_token from /files/settings.txt so we can call the API for information
It also resizes the command prompt window to the correct size for the program
(Ex. debuginfo, Shows additional debugging information when errors are encountered if it is useful) 

Variables:
ACCESS_TOKEN/access_token: used to store the access token we use for getting API information.
debuginfo: on certain errors, shows additional custom debugging information.
extended_debug_info: extended debug information for certain errors (Ex. 204)
errorcount: logs how many errors the program has encountered, minus expired API access tokens.
json_resp: this is where the json response from the spotify API is stored to be used in get_api_information()
sleeptime: how long the program will wait inbetween API requests (default values: 0.5s, 1s)
progresstype: this has two functions. "Remainder" will show the duration/-elapsed time. Any other value will show elapsed time/duration
SPOTIFY_GET_CURRENT_TRACK_URL: this is the URL that we use to get the API information. Do not change this.
clipboard: if Pyperclip is installed, this will determine whether or not your current song is copied to your clipboard. Use Boolean values to toggle.

Known Issues:
os.system("title XXXXX")
    If there is a forbidden character in the artist(s) names, the command will fail to execute and display the previously playing song in the title,
    and if there was no previously playing song, the title will say "Main Program"

Needs additional testing:
204 Error handler
    While the program will retrieve a song after 204 error is cleared, it isn't fully tested yet and it isn't known
    if it is bulletproof yet.
Last Edited 7/26/21 8:58PM CST