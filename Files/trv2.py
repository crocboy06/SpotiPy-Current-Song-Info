import configparser, spotipy, os
from configparser import ConfigParser
from spotipy.oauth2 import SpotifyOAuth
import time
import pyperclip
config_object = ConfigParser()
config_object.read("config.ini")
conf_vars = config_object["CONFVARS"]

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="cc0e1614b21a442cafbda6a297331f91",
            client_secret="7e92d1d35b0d45eb8442a0d336babc48",
            redirect_uri="http://localhost:5000/redirect",
            scope="user-read-currently-playing",
            )

try:
    sp_oauth = create_spotify_oauth()
    new_token = sp_oauth.refresh_access_token(conf_vars['refresh_token'])
    old_token = conf_vars['access_token'][:10]
    conf_vars['access_token'] = new_token['access_token']
    conf_vars['refresh_token'] = new_token['refresh_token']
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    if old_token == conf_vars['access_token']:
        print("Token Refresh Unsuccessful. Old and new tokens are identical.")
        print(0/0)
    print(f"Old Token: {old_token}...")
    print(f"New Token: {conf_vars['access_token'][:10]}...")
    print("Refresh Successful.")
    time.sleep(5)
except:
    os.system("cls")
    from time import sleep
    print("Unknown error occured while trying to refresh access token.\nTrying again in 5 seconds.")
    sleep(5)
    try:
        sp_oauth = create_spotify_oauth()
        new_token = sp_oauth.refresh_access_token(conf_vars['refresh_token'])
        conf_vars['access_token'] = new_token['access_token']
        conf_vars['refresh_token'] = new_token['refresh_token']
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
    except:
        print(0/0)
       
