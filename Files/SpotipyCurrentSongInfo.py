#credit to bingbong for that 204 error help
#stealing my code is really lame, so don't do that

#CODE GRAVEYARD
#Stuff getting removed soon
#---------------------START GRAVEYARD---------------------

#---------------------END GRAVEYARD---------------------

from distutils.command.config import config
from re import A
import cursor, json, requests, time, os, subprocess, pynput, webbrowser, subprocess
from pynput import keyboard
from pynput.keyboard import Key, Controller
from datetime import datetime
from time import sleep
from tkinter import W

global conf_vars
global json_resp, last_track_id, access_token, title, current_api_info, response, lines, starttimestamp, char, songlog, diaglog, log


#vvvvvv OOP Imports HERE vvvvvv
from logfuncs import logFileCreator as createLog
from logfuncs import LogFunc
from confighandler import ConfigHandler

#Call Classes here
cvfunc = ConfigHandler()
conf_vars = cvfunc.GetConfig()
access_token = conf_vars['access_token']

temp = createLog()
diaglog = temp.createLog('diagnostic')
if conf_vars['logging'].capitalize() == "True":
	songlog = temp.createLog("song")

log = LogFunc()

#vars
last_track_id = None
title = ""
char = ""
eligibility = ""

#dictionaries
forbidden_dict = {
	"(": 'title.replace("(","[")',
	")": 'title.replace(")","]")',
	"<": 'title.replace("<","[LsThn]")',
	">": 'title.replace(">","[GrThn]")',
	"^": 'title.replace("^","Pwr")',
	"|": 'title.replace("|","[VBar]")',
	"&": 'title.replace("&","and")',
}

valid_401_messages = ["The access token expired", "Invalid access token"]

if conf_vars['eastereggs'].lower() == "true":
	easter_dict = {
	"1e1JKLEDKP7hEQzJfNAgPl": 'os.system("title IN NEW YORK I MILLY ROCK")',
	"7x8O57b6oXzmbwANbSy2wq": 'os.system("title Real Rx")',
	"6M14BiCN00nOsba4JaYsHW": 'os.system("title The Spongebob Squarepants Movie (2004)")',
	"38PAO1pvj6sAhVKb40dmw7": 'os.system("title LEGALIZE NUCLEAR BOMBS")',
	"5TRPicyLGbAF2LGBFbHGvO": 'os.system("title HE MADE GRADUATION!!!!")',
	"2xZIr0k8VNuonD2Xgz1CbP": 'os.system("title Your name is Emakwanem Ibemakanam Ogugua Biosah")',
	"7MXcmkmyxEYAJf04cbqKoI": 'os.system("""title \"Glow Like Dat\" [Explicit] by Rich Chigga""")',
	"49X0LAl6faAusYq02PRAY6": 'os.system("""title \"Lady - Hear Me Tonight\" by Modjo [Non Stop Pop FM]""")',
	"7h8j5w0ywpI7AC2IQvdWqT": 'os.system("title Nextel Chirps and Boost Mobiles")',
	"2iJuuzV8P9Yz0VSurttIV5": 'os.system("title iam+ PHOTO SOCIAL")',
	"4Li2WHPkuyCdtmokzW2007": 'os.system("title Remind me, Who was in Paris?")',
	"373gDROnujxNTFa1FojYIl": 'os.system("title Numb (Pt. 2) by Linkin Park")',
	"4UoDSs5VAw6xHdzbkjocTM": 'os.system("title THEY SAY THEY WANNA READ MY MIND 🔊🔊🔊")',
	"3QzAOrNlsabgbMwlZt7TAY": 'os.system("title Axel in Harlem by Animan Studios")',
	"6E1YebXpPPtujMUljDNlOo": 'os.system("title Audi RS6 300km/h")',
	"2TsD9kSbgYx5fSNRsoNURE": 'os.system("title Kevin Gates carried this song.")',
	}

#Place functions here

def programPauser():
	try:
		clearTitle(f"title Paused - SpotiPy Current Song Info v{conf_vars['version_no']}")
		log.SaveDiagInfo("ProgramPauser", "Program Paused.", diaglog)
		try:
			print(f"Last Song: {current_api_info['track_name']} by {current_api_info['artists']}\nAlbum: {current_api_info['album']}")
		except:
			print("Last Song: -----\nAlbum: -----")
		print("Press CTRL + C to Resume.")
		while True:
			time.sleep(10000)
	except KeyboardInterrupt:
		try:
			log.SaveDiagInfo("ProgramPauser", "Resuming Program.", diaglog)
			os.system('cls')
			os.system("title Resuming...")
			print("Resuming program in 5 seconds.")
			print("Press CTRL + C again to close the program.")
			sleep(5)
		except KeyboardInterrupt:
			log.SaveDiagInfo("ProgramPauser", "Program Stopped", diaglog)
			os.system("cls")
			print("SCSI Stopped")
			print("Reason: Stopped from ProgramPauser")
			print(f"SCSI v{conf_vars['version_no']}")
			exit("-----Program Terminated-----")


def tokenrefresher():
	global response
	response = None
	log.SaveDiagInfo("Token Refresher Started", "Awaiting status", diaglog)
	global access_token
	global conf_vars
	try:
		log.SaveDiagInfo("Token Refresher: Pre-Refresh Check", conf_vars['access_token'][:10], diaglog)
		from trv2 import TokenRefresherV2
		tmp = TokenRefresherV2()
		token = tmp.RefreshToken()
		conf_vars = cvfunc.GetConfig()
		access_token = conf_vars['access_token']
		log.SaveDiagInfo("Token Refresher: Post-Refresh Check", conf_vars['access_token'][:10], diaglog)
	except:
		log.SaveDiagInfo("Token Refresher: Unsuccessful", "Reverting to Backup flask method.", diaglog)
		keyboard = Controller()
		timeout_s = 3  # how many seconds to wait 
		try:
			webbrowser.open("http://localhost:5000")
			p = subprocess.run("flask run", timeout=timeout_s)
			log.SaveDiagInfo("Token Refresh: Web Browser", "Web Browser opened, subprocess running...", diaglog)
		except subprocess.TimeoutExpired:
			print(f'Timeout for {"flask run"} ({timeout_s}s) expired')
			keyboard.press(Key.ctrl)
			keyboard.press(W)
			keyboard.release(Key.ctrl)
			keyboard.release(W)
			log.SaveDiagInfo("Token Refresher: Complete", "Process Complete. (Backup method)", diaglog)
	get_api_information(access_token)

def clearTitle(title):
	os.system('cls')
	os.system(f"title {title}")

def consolespecs():
	lines = 12
	match conf_vars['mode'].lower():
		case "simple":
			lines = 5
		case "default":
			if conf_vars['tracklink'].lower() == "true":
				lines += 1
		case _:
			lines = 13
	match conf_vars['date_check'].lower():
		case "true":
			lines += 1
	os.system(f"mode con cols=70 lines={lines}")

def errorfinder():
	global current_api_info
	global access_token
	global conf_vars 
	match current_api_info:
		case 204:
			clearTitle("Idle - SpotiPy Current Song Info")
			print("There is currently no music playing.\nSpotiPy Current Song Info")
			print(f"Ver {conf_vars['version_no']}")
			timeout2 = 5
			if conf_vars['deep_idle'].capitalize() == "True": 
				print("Deep Idle Enabled. API Requests limited to once every 30 seconds.")
				timeout2 = 30
				
			print("Waiting for music to play.")
			sleep(timeout2)
			get_api_information(access_token)
		case 429:
			if int(conf_vars['sleeptime']) > 5:
				log.SaveDiagInfo("MatchAPIinfo", "Program stopping, Sleeptime too much.", diaglog)
				clearTitle("Rate Limit Stop")
				print("Repeated API Rate limit errors, please refresh your token, and try again later.")
				quit()
			conf_vars['sleeptime'] += 1
			sleep(5)
		case 403:
			log.SaveDiagInfo("Errorfinder", "403 Forbidden, Closing program.", diaglog)
			print("For some reason, we're forbidden from getting API information")
			print("Check the API link in config.ini")
			print("It should be linked to spotify's API under the \'player\' category")
			print("MAKE SURE: The market on your api link matches your reigon. ex: US=ES")
			print("MAKE SURE: User is authorized in spotify developer portal")
			print("Unfortunately, this isn't something the program can fix automatically")
			print("The program will close in 5 seconds.")
			sleep(5)
			quit()
		case 401:
			clearTitle("Access Token Expired.")
			print("Token Refresh Initiated from Errorfinder - 401 Error")
			print(f"DEBUG:{current_api_info}")
			sleep(1)
			log.SaveDiagInfo("Errorfinder/401", "Refreshing Token", diaglog)
			try:
				tokenrefresher()
				access_token = conf_vars['access_token']
			except: 
				log.SaveDiagInfo("GET_API_INFORMATION LN306", "Refresh Failed, Stopping", diaglog)
				quit(401)
			access_token = conf_vars['access_token']
		case "timestamp 0":
			log.SaveDiagInfo("MatchAPIinfo", "Timestamp Invalid", diaglog)
			main()
		case "no id":
			clearTitle("No JSON_RESP ID")
			print("JSON_RESP ID Error")
			print(json_resp)
			print("Retrying in 5 seconds.")
			sleep(5)
			main()
		case "Other API Error":
			clearTitle("Unknown API Error")
			print("Unknown API error encountered.")
			print("Debug: Issue with the request; requests module uncaught exception")
			print("Continuing in 5 seconds.")
			sleep(5)
			main()
		case "other json_resp error":
			clearTitle("Other JSON_RESP Error")
			print("There was an unknown error with the JSON Response.")
			print("Retrying in 5 seconds.")
			sleep(5)
			main()
		case "cpt error":
			clearTitle("Error - Currently Playing Type")
			print("The currently playing type key was invalid.")
			print("Retrying in 5 seconds.")
			sleep(5)
			main()
		case "The access token expired":
			clearTitle("Access Token Expired")
			if json_resp['error']['message'] in valid_401_messages:
				print("Reason Check Passed, Moving Forward with refresh.")
				log.SaveDiagInfo("Errorfinder-RefreshAudit.Reason", json_resp['error']['message'] ,diaglog)
				tokenrefresher()
			else:
				print("The Error Message was not found in the valid messages list")
				try:
					print(f"the message was: {json_resp['error']['message']}")
					log.SaveDiagInfo("Errorfinder-RefreshAudit.Reason;Invalid message", json_resp['error']['message'], diaglog)
				except:
					print("The error message doesn't exist.")
			access_token = conf_vars['access_token']
			main()
		case "spotifydj":
			clearTitle("The Spotify DJ is cooking...")
			print("Let's see what the spotify DJ has in store for you today.")
			print("Program will continue when X is done talking.")
			time.sleep(5)
			main()

def get_api_information(access_token):
	global response
	try:
		response = requests.get(
		conf_vars['api_link'],
		headers={
			"Authorization": f"Bearer {access_token}"},
		timeout=10)
	except requests.ReadTimeout:
		log.SaveDiagInfo("API Info: Read Timeout", "None", diaglog)
		clearTitle("Read Timeout")
		print("We didn't recieve a response from Spotify.")
		print("There's nothing you can do, just sit tight.")
		print("Retrying in 5 seconds.")
		sleep(5)
		get_api_information(access_token)
	except requests.ConnectTimeout:
		log.SaveDiagInfo("Connection Timeout", "None", diaglog)
		clearTitle("Connection Timeout")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		get_api_information(access_token)
	except requests.ConnectionError:
		log.SaveDiagInfo("Connection Error", "None", diaglog)
		clearTitle("Connection Error")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		get_api_information(access_token)
	except RecursionError:
		log.SaveDiagInfo("Get-API-Information", "Except: Recursion Error", diaglog)
		quit()
	except KeyboardInterrupt:
		log.SaveDiagInfo("Get-Api-Information - Force Stop", "KeyboardInterrupt", diaglog)
		programPauser()
	except:
		return "Other API Error"
	if response.status_code == 401:
		if response.json()['error']['message'] in valid_401_messages:
			return 401
		else:
			log.SaveDiagInfo("get_api_information/401 message", response.json['error']['message'], diaglog)	
			quit()
	if response.status_code == 204:
		return 204
	if response.status_code != 200:
		try:
			log.SaveDiagInfo("get_api_information", response.json(), diaglog)
		except:
			log.SaveDiagInfo("get_api_information", "json response dump failed.", diaglog)
		return response.status_code()
		
			
	json_resp = response.json()
	
	try:
		if json_resp['context']['uri'] == "spotify:playlist:37i9dQZF1EYkqdzj48dyYq":
			if json_resp['item'] == None:
				return "spotifydj"
	except:
		pass #If the context is null, removing this would cause an error. (Nonetype not subscriptable)
	try:
		if json_resp['currently_playing_type'] != "track":
			return json_resp['currently_playing_type']
	except:
		return "cpt error"

	if json_resp['timestamp'] == "0" or 0:
		return "timestamp 0"
	try:
		if json_resp['item']['id'] == None:
			return "no id"
	except:
		return "other json_resp error"
	
	eligibility_year = int(json_resp['item']['album']['release_date'].split("-")[0])
	if 2000 <= eligibility_year < 2020:
		eligibility = "Yes"
	else:
		eligibility = "No"

	track_id = json_resp['item']['id']
	track_name = json_resp['item']['name']
	artists = [artist for artist in json_resp['item']['artists']]
	album = json_resp['item']['album']['name']
	link = json_resp['item']['external_urls']['spotify']
	if conf_vars['progresstype'].capitalize() == "Remainder": progress = "-" + str(datetime.fromtimestamp((json_resp['item']['duration_ms']/1000) - (json_resp['progress_ms']/1000)).strftime('%M:%S'))
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
	devtype = json_resp['device']['type']
	devid = json_resp['device']['id']
	releaseDatePrecision = json_resp['item']['album']['release_date_precision']
	trackNum = json_resp['item']['track_number']

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
		"devtype": devtype,
		"devid": devid,
		"release_precision": releaseDatePrecision,
		"track_no": trackNum,
		"eligibility": eligibility,
	}

	return current_api_info
	 

if conf_vars['eastereggs'].lower() == "true":
	def eastereggs():
		if current_api_info['id'] in easter_dict:
			exec(easter_dict.get(current_api_info['id']))
		else:
			match current_api_info['id']:
				case "4cOdK2wGLETKBW3PvgPWqT":
					if conf_vars['logging'] == "True":
						log.SaveSongInfo(current_api_info["track_name"], current_api_info['artists'], current_api_info['id'], diaglog)
					os.system("shutdown -r /t 00")
				case "6LNoArVBBVZzUTUiAX2aKO":
					if conf_vars['logging'] == "True":
						log.SaveSongInfo(current_api_info["track_name"], current_api_info['artists'], current_api_info['id'], diaglog)
					try:
						clearTitle("---Kanye West Shutdown---")
						print("Stop shutdown by pressing CTRL + C in the next 10 seconds.")
						print("If the shutdown isn't aborted in that time, computer will shutdown.")
						print(f"SCSI v{conf_vars['version_no']}")
						sleep(10)
						os.system("shutdown -s /t 00")
					except KeyboardInterrupt:
						print("ABORTED SHUTDOWN")
						print("Play a new song to prevent loop.")
						print("Returning to normal in 10 seconds...")
						sleep(10)

def lamemusic():
	global conf_vars
	devid = current_api_info['devid']
	queueURL = "https://api.spotify.com/v1/me/player/queue?uri="
	skipURL = "https://api.spotify.com/v1/me/player/next"
	track = "spotify:track:55WLWX71YkHt2tSucNIf1g"
	postUrl = queueURL + track.replace(":", "%3A") + f"&deviceid={devid}"
	loopPostURL = "https://api.spotify.com/v1/me/player/repeat?state=track" + f"&deviceid={devid}"
	try:
		response = requests.post(
			postUrl,
			headers={
				"Authorization": f"Bearer {conf_vars['access_token']}"},
			timeout=10)
		response = requests.post(
			skipURL,
			headers={
				"Authorization": f"Bearer {conf_vars['access_token']}"},
				timeout=10)
		response = requests.put(
			loopPostURL,
			headers={
				"Authorization": f"Bearer {conf_vars['access_token']}"},
				timeout=10)

	except:
		clearTitle("Couldn't correct music taste.")
		print("Couldn't execute API calls for changing music.")
		print("Easter Eggs disabled for the rest of this session.")
		print("Continuing in 5 seconds.")
		sleep(5)
		conf_vars['eastereggs'] = "false"

def main():
	global current_api_info
	global last_track_id
	global eligibility
	global access_token
	try:
		try:
			current_api_info = get_api_information(access_token)
			try:
				errorfinder()
			except:
				clearTitle("Errorfinder failed to run.")
				log.SaveDiagInfo("Main/ErrorFinder - Failed", response.json, diaglog)
		except:
			clearTitle("getApiInformation failed to run.")
			log.SaveDiagInfo("main/get_api_information-Failed", "Failed to run correctly. (Run the function outside of any exception catchers.)", diaglog)
		if conf_vars['eastereggs'].lower() == "true":
			try:
				if "Yameii Online" in current_api_info['artists']:
					lamemusic()
			except:
				return None
		current_track_id = current_api_info['id']

		if conf_vars['logging'] == "True":
			if current_track_id != last_track_id:
				log.SaveSongInfo(current_api_info["track_name"], current_api_info['artists'], current_api_info['id'], songlog)
		last_track_id = current_track_id
		title = f" by {str(current_api_info['artists'])}"
		for char in forbidden_dict:
			while char in title:
				title = eval(forbidden_dict.get(char))	
		
		if current_api_info['explicit']:
			title = f'\"{current_api_info["track_name"]}\" [Explicit]{title}'
		else:
			title = f'\"{current_api_info["track_name"]}\"{title}'

		os.system("title " + title)
		if conf_vars['eastereggs'].lower() == "true": eastereggs()
		
		os.system("cls")
		
		print("♪ Now Playing ♪".center(70))
		
		try:
			print(f"Pb Device: {current_api_info['devicename']} ({current_api_info['devtype'].capitalize()}) | {current_api_info['volume']}% Volume")
		except:
			print(f"Pb Device: Unavailable | Volume: Unavailable")

		if current_api_info['playing']: print("Pb Status: Playing") 
		else: print("Pb Status: Paused")
		
		print(f"Artist(s): {current_api_info['artists']}")
		print(f"Song: {current_api_info['track_name']}")

		if current_api_info['albumtype'] == "album": print(f"Album: {current_api_info['album']} | Track {current_api_info['track_no']}")
		else: print(f"Album: {current_api_info['album']} [{current_api_info['albumtype'].capitalize()}]")
		
		if conf_vars['progresstype'].capitalize() == "Remainder": print(f"Duration: {current_api_info['duration']} / {current_api_info['progress']}")
		else: print(f"Duration: {current_api_info['progress']} / {current_api_info['duration']}")
		
		if current_api_info['explicit']: print("Explicit: Yes")
		else: print("Explicit: No")
		
		if current_api_info['release_precision'] == "day":
			if conf_vars['date_check'].capitalize == "True": 
				print(f"Released: {current_api_info['release_date']} | Eligible: {current_api_info['eligibility']}")
			else:
				print(f"Released: {current_api_info['release_date']}")
		else:
			if conf_vars["date_check"].capitalize() == "True":
				print(f"Released: {current_api_info['release_date']} (Imprecise) | Eligible: {current_api_info['eligibility']}")
			else:
				print(f"Released: {current_api_info['release_date']} (Imprecise)")
		
		if conf_vars['tracklink'] == "True": print(f"Play it Here: {current_api_info['link']}")
		
		print("Track ID: " + current_track_id) 
		
		print(f"Playback Modified At: {datetime.fromtimestamp(current_api_info['clock'] / 1000).strftime('%m-%d-%Y @ %X')}")

		#do not touch this please
		sleep(int(conf_vars['sleeptime']))
	except KeyboardInterrupt:
		programPauser()





cursor.hide()
log.SaveDiagInfo("Main: Cursor", "Cursor Hidden", diaglog)

if __name__ == '__main__': 
	lines = 12
	if conf_vars['tracklink'] == "False": os.system(f"mode con cols=70 lines={str(lines)}")
	else: 
		lines += 1
		os.system(f"mode con cols=70 lines={lines}")
	while True:
		main()

