#credit to bingbong for that 204 error help
#stealing my code is really lame, so don't do that (lmao just do it anyway this is garbage probably)(its getting better tho)
from distutils.command.config import config
import cursor, json, requests, time, os, subprocess, pyperclip, pynput, webbrowser
from tkinter import W
from pynput import keyboard
from pynput.keyboard import Key, Controller
from datetime import datetime
from configparser import ConfigParser
global songlog, json_resp, last_track_id, access_token, sleeptime, errorcount, debuginfo, extended_debug_info, SPOTIFY_GET_CURRENT_TRACK_URL,progresstype
global clipboard, silenterrors, starttimestamp, version_no
Token = open('settings.txt', "r")
Token.seek(0)
ACCESS_TOKEN = Token.read()
Token.close
access_token = ACCESS_TOKEN
os.system("mode con cols=70 lines=13")
cursor.hide()
#Configuration and storage variables
starttimestamp = str(datetime.fromtimestamp(datetime.now().timestamp()).strftime("%m-%d-%Y, %H-%M-%S"))
config_object = ConfigParser()

config_object['CONFVARS'] = {
	"debuginfo": True,
	"extended_debug_info": True,
	"progresstype": "Duration",
	"sleeptime": 0,
	"clipboard": False,
	"silenterrors": True,
	"version_no": "1.0.5",
}
config_object.read("config.ini")
conf_vars = config_object['CONFVARS']
with open('config.ini', 'w') as conf:
    config_object.write(conf)

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
keyboard = Controller()
last_track_id = None
print("Startup Complete")
print("Starting Program")
songlog = open("logs/" + starttimestamp + ".txt", "w+")
songlog.write("SONG LOG FOR SESSION")
songlog.close()
def tokenrefresher():
	global access_token
	from pynput import keyboard
	from pynput.keyboard import Key, Controller
	keyboard = Controller()
	timeout_s = 3  # how many seconds to wait 
	try:
		webbrowser.open_new('http://localhost:5000')
		p = subprocess.run("flask run", timeout=timeout_s)
	except subprocess.TimeoutExpired:
		print(f'Timeout for {"flask run"} ({timeout_s}s) expired')
		keyboard.press(Key.ctrl)
		keyboard.press(W)
		keyboard.release(Key.ctrl)
		keyboard.release(W)
	Token = open('settings.txt', "r")
	Token.seek(0)
	ACCESS_TOKEN = Token.read()
	Token.close
	access_token = ACCESS_TOKEN
	os.system("cls")


def errorfinder():
	global sleeptime
	global errorcount
	global ACCESS_TOKEN
	access_token = ACCESS_TOKEN
	try:
		#This was implemented to prevent "NoneType is not subscriptable" TypeError.
		#This error was found to occur when the program calls to the API to try and get current song information while the user is inbetween songs.
		#Most likely the inbetween period is over, so lets get song information after we wait 5 seconds
		if json_resp['timestamp'] == 0:
			if not silenterrors:
				os.system("cls")
				os.system("title " + "Error")
				print("Whoops! You caught us at a bad time.")
				print("Something's gone wrong.")
				print("We'll retry this in 5 seconds.")
				if debuginfo: print("Error Code: TIMESTAMP_EQUAL_TO_ZERO")
				if extended_debug_info: print("Most common cause is that the user is inbetween songs.")
				time.sleep(5)
				#Once the error has been handled, and the user knows, refresh the current song and get a new JSON response to clear the error
			get_api_information(ACCESS_TOKEN)
	except:
		#If the error is something else, like an API Rate limit, it will follow through this, and give some error specific information for common problems.
		#If the JSON response has an error, let's tell the user, and handle it.
		os.system("cls")
		os.system("title " + "Oops!")
		print("We've encountered an error.")
		print("The Error code we recieved is: " + str(json_resp['error']['status']))
		print("Additional information: " + str(json_resp['error']['message']))
		match json_resp['error']['status']:
			case 429:
				if debuginfo:
					apirate = round(30/sleeptime,0)
					print("APIINFO: " + str(apirate) + "/30s @ " + str(sleeptime) + "s DELAY")
				if sleeptime > 5:
					os.system("cls")
					print("Repeated API Rate limit errors, please refresh your token, and try again later.")
					quit()
				sleeptime += .250
			case 401:
				os.system("cls")
				tokenrefresher()
				print("Access Token Set")
				print("Successfully refreshed token.")
				Token = open('settings.txt', "r")
				Token.seek(0)
				ACCESS_TOKEN = Token.read()
				Token.close
				access_token = ACCESS_TOKEN
		errorcount += 1
		print("Error Count:", errorcount)
		print("Retrying in 1 second.")
		time.sleep(1)
		get_api_information(ACCESS_TOKEN)
# vvvv NOT WORKING vvvv
def responsecodeintercept(method, sleeptime, access_token, currcode):
	if method == "NoContent":
		match currcode:
			case 204:
				os.system("title Nothing Playing")
				print("There is no music playing.")
				print("\n\n\n\n\n\n\n\n")
				print("SpotiPy Current Song Info")
				print("Ver " + version_no)
				print("Waiting for music to play...")
				while currcode == 204:
					response = requests.get(
					SPOTIFY_GET_CURRENT_TRACK_URL,
					headers={
						"Authorization": f"Bearer {access_token}"
					})
					currcode = response.status_code
					time.sleep(sleeptime)
		#other features WIP
	if method == "Other":
		match currcode:
			case 429:
				print("API Rate limit error.")
				print("The program has sent too many requests.")
				print("We'll attempt to fix this.")
				sleeptime += .250
			case 401:
				print("The Access Token we have is expired.")
				print("We'll try to refresh it now.")
				tokenrefresher()
				Token = open('settings.txt', "r")
				Token.seek(0)
				ACCESS_TOKEN = Token.read()
				Token.close
	get_api_information(access_token)
# ^^^^ NOT WORKING ^^^^

def get_api_information(access_token):
	response = requests.get(
		SPOTIFY_GET_CURRENT_TRACK_URL,
		headers={
			"Authorization": f"Bearer {access_token}"
		})
	if response.status_code == 204:
		os.system("cls")
		os.system("title Nothing Playing")
		print("There is currently no song playing.")
		print("\n\n\n\n\n\n\n")
		print("SpotiPy Current Song Info.")
		print("Ver " + conf_vars['version_no'])
		print("Waiting for music to play...")
		while response.status_code == 204:
			response = requests.get(
			SPOTIFY_GET_CURRENT_TRACK_URL,
			headers={
				"Authorization": f"Bearer {access_token}"
			})
			time.sleep(int(conf_vars['sleeptime']))
		get_api_information(access_token)
	global json_resp
	json_resp = response.json()
	errorfinder()
	track_id = json_resp['item']['id']
	track_name = json_resp['item']['name']
	artists = [artist for artist in json_resp['item']['artists']]
	album = json_resp['item']['album']['name']
	link = json_resp['item']['external_urls']['spotify']
	if conf_vars['progresstype'] == "Remainder": progress = "-" + str(datetime.fromtimestamp((json_resp['item']['duration_ms']/1000) - (json_resp['progress_ms']/1000)).strftime('%M:%S'))
	else: progress = str(datetime.fromtimestamp(json_resp['progress_ms'] / 1000).strftime('%M:%S'))
	duration = str(datetime.fromtimestamp(json_resp['item']['duration_ms'] / 1000).strftime('%M:%S'))
	playing = json_resp['is_playing']
	explicit = json_resp['item']['explicit']
	releasedate = json_resp['item']['album']['release_date']
	artist_names = ', '.join([artist['name'] for artist in artists])
	device = json_resp['device']['name']
	volume = json_resp['device']['volume_percent']
	albumtype = json_resp['item']['album']['album_type']
	clock = json_resp['timestamp']

	current_api_info = {
		"id": track_id,
		"track_name": track_name,
		"artists": artist_names,
		"link": link,
		"album": album,
		"duration": duration,
		"progress": progress,
		"playing": playing,
		"explicit": explicit,
		"release_date": releasedate,
		"devicename": device,
		"volume": volume,
		"albumtype": albumtype,
		"clock": clock,
	}

	return current_api_info

def eastereggs():
	match current_api_info['id']:
		case "4cOdK2wGLETKBW3PvgPWqT":
			songlog = open('logs/' + starttimestamp + ".txt", "a")
			songlog.write(current_api_info['id'] + "LAAAAME GOT REBOOTED")
			songlog.close()
			os.system("shutdown -r /t 00")
		case "6LNoArVBBVZzUTUiAX2aKO":
			songlog = open('logs/' + starttimestamp + ".txt", "a")
			songlog.write(current_api_info['id'] + "LAAAAME GOT SHUTDOWN")
			songlog.close()
			os.system("shutdown -s /t 00")
		case "1e1JKLEDKP7hEQzJfNAgPl":
			os.system("title IN NEW YORK I MILLY ROCK")
		case "7K1HH9OC6nZlJqrGnr8r1g":
			os.system("title Real Rx")
		case "6M14BiCN00nOsba4JaYsHW":
			os.system("title The Spongebob Squarepants Movie (2004)")

def main():
	global current_api_info
	global last_track_id
	current_api_info = get_api_information(ACCESS_TOKEN)
	current_track_id = current_api_info['id']
	
	if current_track_id != last_track_id:
		songlog = open("logs/" + starttimestamp + ".txt", "a")
		songlog.write("\n")
		songlog.write(current_api_info['id'])
		songlog.close()
		last_track_id = current_track_id
	

	#Please, someone make this a switch statement.
	if "(" in current_api_info['artists']:
		os.system("title Currently Playing Track")
	elif ")" in current_api_info['artists']:
		os.system("title Currently Playing Track")
	elif "<" in current_api_info['artists']:
		os.system("title Currently Playing Track")
	elif ">" in current_api_info['artists']:
		os.system("title Currently Playing Track")
	elif "|" in current_api_info['artists']:
		os.system("title Currently Playing Track")
	elif "^" in current_api_info['artists']:
		os.system("title Currently Playing Track")
	else:
		os.system("title " + '"' + str(current_api_info['track_name']) + '"' + " by " + str(current_api_info['artists']))
	#Please.

	eastereggs()

	os.system("cls")
	print("                         ♪ Now Playing ♪                              ")
	
	print("Playback Device: " + current_api_info['devicename'] + " @ " + str(current_api_info['volume']) + "% Volume")

	if current_api_info['playing']: print("Playback Status: Playing")
	if not current_api_info['playing']: print("Playback Status: Paused")
	
	print("Artist(s): " + current_api_info['artists'])
	print("Song: " + current_api_info['track_name'])

	if current_api_info['albumtype'] == "album": print("Album: " + current_api_info['album'])
	if current_api_info['albumtype'] != "album": print("Album: " + current_api_info['album'] + " [" + current_api_info['albumtype'].capitalize() + "]")
	
	if conf_vars['progresstype'] == "Remainder": print("Duration: " + current_api_info['duration'] + " / " + current_api_info['progress'])
	if conf_vars['progresstype'] != "Remainder": print("Duration: " + current_api_info['progress'] + " / " + current_api_info['duration'])
 
	if current_api_info['explicit']: print("Explicit: Yes")
	if not current_api_info['explicit']: print("Explicit: No")
	
	print("Released: " + current_api_info['release_date'])
	print("Play it Here: " + current_api_info['link'])
	print("TrackID: " + current_track_id) 
	print("Last Song Change: " + str(datetime.fromtimestamp(current_api_info['clock'] / 1000).strftime("%m-%d-%Y, %H:%M:%S")))
	
	if conf_vars['clipboard']: pyperclip.copy(current_api_info['track_name'] + " By " + current_api_info['artists'])
	
	#do not touch this please
	time.sleep(int(conf_vars['sleeptime']))


if __name__ == '__main__': 
	while True:
		main()