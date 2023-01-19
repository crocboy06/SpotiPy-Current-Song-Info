from lib2to3.pgen2 import token
from re import A
from turtle import title
from flask import Flask, request, url_for, session, redirect, send_from_directory
import spotipy, requests, time, os
from spotipy.oauth2 import SpotifyOAuth
from configparser import ConfigParser
app = Flask(__name__)

app.secret_key = "FUCKINGPASSWORD"
app.config['SESSION_COOKIE_NAME'] = "Connor, The Android, Sent by CyberLife"
TOKEN_INFO = "token_info"

@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')

@app.route('/skip')
def skip():
    global token_info
    SPOTIFY_SKIP_URL = "https://api.spotify.com/v1/me/player/next"
    response = requests.post(
		SPOTIFY_SKIP_URL,
		headers={
			"Authorization": f"Bearer {token_info['access_token']}"
		})
    return redirect('/currentlyPlaying')


@app.route('/runitback')
def replay():
    global token_info
    SPOTIFY_RIB_URL = "https://api.spotify.com/v1/me/player/seek?position_ms=0"
    response = requests.put(
		SPOTIFY_RIB_URL,
		headers={
			"Authorization": f"Bearer {token_info['access_token']}"
		})
    return redirect('/currentlyPlaying')

@app.route('/refreshtoken')
def refreshtoken():
    get_token2()
    return redirect('/currentlyPlaying')

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)
    


@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect('/refreshtoken')

@app.route('/currentlyPlaying')
def currentlyPlaying():
    global token_info
    try:
        token_info = get_token()
    except:
        print("Re-Authenticating")
        redirect("https://google.com")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp.current_playback()


def get_token2():
    global token_info
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    config_object = ConfigParser()
    config_object.read("config.ini")
    conf_vars = config_object["CONFVARS"]
    conf_vars['access_token'] = token_info['access_token']
    conf_vars['refresh_token'] = token_info['refresh_token']
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    return token_info

def get_token():
    global token_info
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time)

    is_expired = token_info['expires_at'] - now <60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    config_object = ConfigParser()
    config_object.read("config.ini")
    conf_vars = config_object["CONFVARS"]
    conf_vars['access_token'] = token_info['access_token']
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="cc0e1614b21a442cafbda6a297331f91",
            client_secret="7e92d1d35b0d45eb8442a0d336babc48",
            redirect_uri="http://localhost:5000/redirect",
            scope="user-read-currently-playing",
            )