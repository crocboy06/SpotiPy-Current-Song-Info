#credit to bingbong for that 204 error help
#stealing my code is really lame, so don't do that

#CODE GRAVEYARD
#Stuff getting removed soon
#---------------------START GRAVEYARD---------------------

#---------------------END GRAVEYARD---------------------

from distutils.command.config import config
from re import A
import cursor, json, requests, time, os, subprocess, pynput, webbrowser, subprocess, platform
from pynput import keyboard
from pynput.keyboard import Key, Controller
from datetime import datetime
from time import sleep
from tkinter import W
from exceptions import *

global conf_vars
global json_resp, last_track_id, access_token, title, current_api_info, response, lines, starttimestamp, char, songlog, diaglog, log, toBePaused


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
last_track_id, title, char, eligibility, toBePaused, response_valid = None, "", "", "", False, False

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
	"49X0LAl6faAusYq02PRAY6": 'os.system("""title \"Lady - Hear Me Tonight\" by Modjo [Non Stop Pop FM]""")',
	"7h8j5w0ywpI7AC2IQvdWqT": 'os.system("title Nextel Chirps and Boost Mobiles")',
	"2iJuuzV8P9Yz0VSurttIV5": 'os.system("title iam+ PHOTO SOCIAL")',
	"4Li2WHPkuyCdtmokzW2007": 'os.system("title Remind me, Who was in Paris?")',
	"373gDROnujxNTFa1FojYIl": 'os.system("title Numb (Pt. 2) by Linkin Park")',
	"4UoDSs5VAw6xHdzbkjocTM": 'os.system("title THEY SAY THEY WANNA READ MY MIND 🔊🔊🔊")',
	"3QzAOrNlsabgbMwlZt7TAY": 'os.system("title Axel in Harlem by Animan Studios")',
	"6E1YebXpPPtujMUljDNlOo": 'os.system("title Audi RS6 300km/h")',
	"2TsD9kSbgYx5fSNRsoNURE": 'os.system("title Kevin Gates carried this song.")',
	"5xEddMQaqVM8W4iJt2KZw2": 'os.system("title ＮＩＮＥ ＯＮＥ 🎸💫 (Jqho8GJ-7JU)")',
	"4pDZMkTyq5YQNYLIXq0xA0": 'os.system("title GettyImages \ 25 Years")',
	"7MXcmkmyxEYAJf04cbqKoI": "current_api_info['artists'] = 'Rich Chigga'",
	"285pBltuF7vW8TeWk8hdRR": 'os.system("title I STILL SEE YOUR SHADOWS IN MY ROOM")',
	"7m1cNdKABpKy0aAtsKAIGx": 'os.system("title FREE SANTANA BITCH 💯💯💯")',
	"3ZCczSAiyiT3WZMbeWjuzi": 'os.system("title Kazuo Kawasaki 704 Rimless Frames [Grey, SP-51 Lens])'
	}

#Place functions here



def tokenrefresher():
	global response
	response = None
	log.SaveDiagInfo("Token Refresher Started", "Awaiting status", diaglog)
	global access_token
	global conf_vars
	try:
		log.SaveDiagInfo("Token Refresher: [Pre-Refresh Check]", conf_vars['access_token'][:10], diaglog)
		from trv2 import TokenRefresherV2
		tmp = TokenRefresherV2()
		token = tmp.RefreshToken()
		conf_vars = cvfunc.GetConfig()
		access_token = conf_vars['access_token']
		log.SaveDiagInfo("Token Refresher - [Post-Refresh Check]", conf_vars['access_token'][:10], diaglog)
	except:
		log.SaveDiagInfo("Token Refresher: [Unsuccessful]", "Reverting to Backup flask method.", diaglog)
		keyboard = Controller()
		timeout_s = 3  # how many seconds to wait 
		try:
			webbrowser.open("http://localhost:5000")
			p = subprocess.run("flask run", timeout=timeout_s)
			log.SaveDiagInfo("Token Refresh: [Web Browser]", "Web Browser opened, subprocess running...", diaglog)
		except subprocess.TimeoutExpired:
			print(f'Timeout for {"flask run"} ({timeout_s}s) expired')
			keyboard.press(Key.ctrl)
			keyboard.press(W)
			keyboard.release(Key.ctrl)
			keyboard.release(W)
			log.SaveDiagInfo("Token Refresher: [Complete]", "Process Complete. !!!(Backup method)!!!", diaglog)
	sleep(1)
	main()

def clearTitle(title):
	os.system('cls')
	os.system(f"title {title}")

def consolespecs():
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
			print("\nChecking for song info...")
			sleep(1)
			vd = 204
			return vd
		case 429:
			if int(conf_vars['sleeptime']) > 5:
				log.SaveDiagInfo("MatchAPIinfo", "Program stopping, Sleeptime too high.", diaglog)
				quit()
			conf_vars['sleeptime'] += 1
			sleep(5)
		case 403:
			log.SaveDiagInfo("Errorfinder", "403 Forbidden, Closing program.", diaglog)
			print("For some reason, we're forbidden from getting API information")
			print("Check the API link in config.ini")
			print("It should be linked to spotify's API under the \'player\' category")
			print("Make sure the market on your api link matches your reigon. ex: US=ES")
			print("Make sure the user is authorized in spotify developer portal")
			print("Unfortunately, this isn't something the program can fix automatically")
			print("The program will close in 5 seconds.")
			sleep(5)
			quit()
		case 401:
			clearTitle("Access Token Expired.")
			log.SaveDiagInfo("Errorfinder [401]", "Refreshing Token", diaglog)
			try:
				tokenrefresher()
				access_token = conf_vars['access_token']
			except: 
				log.SaveDiagInfo("ErrorFinder [401]", "Refresh Failed, Stopping", diaglog)
				quit(401)
			access_token = conf_vars['access_token']
		case "timestamp 0":
			log.SaveDiagInfo("ErrorFinder [timestamp 0]", "Timestamp Invalid", diaglog)
			main()
		case "no id":
			log.SaveDiagInfo("ErrorFinder [no id]", "No ID present in json_resp", diaglog)
			clearTitle("No JSON_RESP ID")
			print("JSON_RESP ID Error")
			print(json_resp)
			print("Retrying in 5 seconds.")
			sleep(5)
			main()
		case "Other API Error":
			log.SaveDiagInfo("ErrorFinder [Other API Error]", f"API Error Encountered. {current_api_info}", diaglog)
			clearTitle("Unknown API Error")
			print("Unknown API error encountered.")
			print("Debug: Issue with the request; requests module uncaught exception")
			print("Continuing in 5 seconds.")
			sleep(5)
			main()
		case "other json_resp error":
			log.SaveDiagInfo("ErrorFinder [other json_resp error]", "Unknown problem with json_resp", diaglog)
			clearTitle("Other JSON_RESP Error")
			print("There was an unknown error with the JSON Response.")
			print("Retrying in 5 seconds.")
			sleep(5)
			main()
		case "unknown":
			log.SaveDiagInfo("Errorfinder-MatchCase-Unknown (CPT/None)", "In-between songs... (Ignoring)", diaglog)
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
				log.SaveDiagInfo("Errorfinder [The access token expired]", json_resp['error']['message'] ,diaglog)
				tokenrefresher()
			else:
				print("json_resp error message was not found in the valid messages list.")
				try:
					print(f"the message was: {json_resp['error']['message']}")
					log.SaveDiagInfo("Errorfinder [The access token expired]", f"The error message recieved was not in the valid list. {json_resp['error']['message']}", diaglog)
				except:
					print("The error message doesn't exist.")
			access_token = conf_vars['access_token']
			main()
		case "spotifydj":
			clearTitle("The Spotify DJ is cooking...")
			print("Let's see what the Spotify DJ has in store for you today.")
			print("Program will continue when X is done talking.")
			time.sleep(5)
			main()
		case "episode":
			clearTitle("You are playing a Podcast or Video.")
			print("We do not support podcasts or videos.")
			print("Once you play a song, We'll get things rolling.")
			sleep(10)
			log.SaveDiagInfo("Errorfinder [episode]", "Podcast or Video Detected.", diaglog)
def new_get_player_info(access_token):
	global response, toBePaused
	try:
		response = requests.get(
		conf_vars['api_link'],
		headers={
			"Authorization": f"Bearer {access_token}"},
		timeout=10)
	except requests.ReadTimeout:
		raise NoReply
	except requests.ConnectTimeout:
		raise ConnectionBad
	except requests.ConnectionError:
		raise ConnectionBad
	except RecursionError:
		raise RecursionError
	except KeyboardInterrupt:
		raise KeyboardInterrupt
	except:
		raise OtherAPIError
	if response.status_code == 401:
		raise TokenExpired
	if response.status_code == 204:
		raise NoTrack
	if response.status_code != 200:
		try:
			log.SaveDiagInfo("new_get_player_info", f"Status Code:{response.status_code}", diaglog)
		except:
			pass
		raise ResponseCodeInvalid
	#code = response.status_code
	json_resp = response.json()
	try:
		if json_resp['transferring_playback'] == True:
			raise TransferringPlayback
	except:
		pass
	try:
		if json_resp['context']['uri'] == "spotify:playlist:37i9dQZF1EYkqdzj48dyYq":
			if json_resp['item'] == None:
				raise DJPlaying
			if json_resp['currently_playing_type'] != "track":
				raise DJPlaying
	except:
		pass #If the context is null, removing this would cause an error. (Nonetype not subscriptable)
	try:
		if json_resp['currently_playing_type'] != "track":
			raise CurrentlyPlayingType
	except:
		raise CurrentlyPlayingType
	
	if json_resp['timestamp'] == 0:
		raise TimestampInvalid
	try:
		if json_resp['item']['id'] == None:
			raise NullID
	except:
		log.SaveDiagInfo("New_Get_Player_Info", json_resp, diaglog)
		raise JsonResponseError
	
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
	albumtype = json_resp['item']['album']['album_type'].capitalize()
	clock = json_resp['timestamp']
	devtype = json_resp['device']['type'].capitalize()
	devid = json_resp['device']['id']
	releaseDatePrecision = json_resp['item']['album']['release_date_precision']
	trackNum = json_resp['item']['track_number']
	try:
		context = json_resp['context']['uri']
	except:
		pass
	item = json_resp['item']

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
		"item": item,
	}
	try:
		current_api_info['context'] = context
	except:
		pass

	return current_api_info

if conf_vars['eastereggs'].lower() == "true":
	def eastereggs():
		if current_api_info['id'] in easter_dict:
			exec(easter_dict.get(current_api_info['id']))
		else:
			match current_api_info['id']:
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
						clearTitle("Shutdown Aborted.")
						print("Returning to normal in 5 seconds...")
						print("EasterEggs disabled for this session.")
						sleep(5)
						conf_vars['eastereggs'] = "False"
#Something right here is fucky
	def replace_track(self):
		global conf_vars
		from SupplementaryAPI import APIHandler
		q = APIHandler()
		q.QueueTrack(conf_vars['access_token'], "3CkL7Dfv07KjdL1wbC1m8i", current_api_info['devid'])
		q.SkipSong(conf_vars['access_token'])
		q.LoopTrack(conf_vars["access_token"], current_api_info['devid'])


def main():
	global current_api_info
	global toBePaused
	global last_track_id
	global eligibility
	global access_token
	global response_valid
	response_valid = False
	try:
		while response_valid == False:
			try:
				current_api_info = new_get_player_info(access_token)
				try:
					errorfinder()
					response_valid = True
				except KeyboardInterrupt:
					log.SaveDiagInfo("Main - get_player_info" "KeyboardInterrupt [-21] | Pause Variable set to True", diaglog)
					toBePaused = True
				except:
					clearTitle("Errorfinder failed to run.")
					log.SaveDiagInfo("Main - Errorfinder", f"[2nd level exception]\n{response.json}", diaglog)
			except KeyboardInterrupt:
				log.SaveDiagInfo("Main - get_player_info" "KeyboardInterrupt. [post-errorfinder] | Pause Variable set to True", diaglog)
				toBePaused = True
			except NoTrack:
				clearTitle("Idle - SpotiPy Current Song Info")
				print("There is currently no music playing.\nSpotiPy Current Song Info")
				print(f"Ver {conf_vars['version_no']}")
				timeout2 = 5
				if conf_vars['deep_idle'].capitalize() == "True": 
					print("Deep Idle Enabled. API Requests limited to once every 30 seconds.")
					timeout2 = 30
				print("Waiting for music to play.")
				sleep(timeout2)
				print("\nChecking for song info...")
				sleep(1)
			except DJPlaying:
				clearTitle("[Spotify DJ] Your DJ X is talking.")
				print("Let's see what X is cooking.\n Program will resume when X is done talking.")
				sleep(conf_vars['sleeptime'])
			except TimestampInvalid:
				pass
			except ResponseCodeInvalid:
				pass
			except TokenExpired:
				tokenrefresher()
			except ConnectionBad:
				clearTitle("Internet Connection Error.")
				print("There is a problem with the connection to spotify's API.\nPlease check that you're connected to the internet, with internet access.")
			except TransferringPlayback:
				clearTitle("Spotify is transferring playback.")
				print("Please wait while Spotify switches songs.\n\nSpotiPy Current Song Info")
			except OtherAPIError:
				clearTitle("Other API Error")
				print("An unknown API error has occured.")
				log.SaveDiagInfo("main-except-OtherAPIError", "None", diaglog)
			except NoReply:
				log.SaveDiagInfo("main-exception-NoReply", "No reply recieved from Spotify's API.", diaglog)
			except CurrentlyPlayingType:
				clearTitle("SCSI is paused.")
				print("You are currently not playing music.")
				print("This could be a podcast or something else.")
				print("Play some music, and we'll get back on track.")
				log.SaveDiagInfo("main-CurrentlyPlayingType", "None", diaglog)
			except JsonResponseError:
				clearTitle("JSON Response Error")
				print("Something was wrong with Spotify's API response.")
			#except:
			#	log.SaveDiagInfo("Main | New API Grabber", "Catch-All-Exception", diaglog)
			#	clearTitle("Failed to acquire API Information")
			#	print("There was a problem running the new get player info function.\n Check for uncaught custom exceptions.")
		#except:
		#	clearTitle("get_player_info failed to run.")
		#	log.SaveDiagInfo("Main - get_player_info", "[Uncaught Exception]. (Try running the function outside of any exception catchers.)", diaglog)
		if conf_vars['eastereggs'].lower() == "true":
			if "Yameii Online" in current_api_info['artists']:
				try:
					a = replace_track()
				except:
					conf_vars['eastereggs'] = "False"
					log.SaveDiagInfo("Main-Replace_Track()", "Fail Condition; Easter Eggs Disabled.", diaglog)

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
		
		print("===== ♪ Now Playing ♪ =====".center(70))
		
		try:
			print(f"Device: {current_api_info['devicename']} ({current_api_info['devtype']}) | {current_api_info['volume']}% Volume")
		except:
			print(f"Device: Unavailable | Volume: Unavailable")

		if current_api_info['playing']: print("Status: Playing") 
		else: print("Status: Paused")
		
		if len(current_api_info['artists']) > 50: 
			print(f"Artist(s):{current_api_info['artists'][:50]}...")
		else: 
			print(f"Artist(s): {current_api_info['artists']}")
		
		if len(current_api_info['track_name']) > 50:
			print(f"Song: {current_api_info['track_name'][:50]}...")
		else:
			print(f"Song: {current_api_info['track_name']}")

		if current_api_info['albumtype'] == "Album": 
			if len(current_api_info['album']) > 50:
				print(f"Album: {current_api_info['album'][:45]}... | Track {current_api_info['track_no']}")
			else: print(f"Album: {current_api_info['album']} | Track {current_api_info['track_no']}") 
		if current_api_info['albumtype'] != "Album":
			if len(current_api_info['album']) > 50:
				print(f"Album: {current_api_info['album'][:45]}... [{current_api_info['albumtype']}]")
			else: print(f"Album: {current_api_info['album']} [{current_api_info['albumtype']}]") 
		
		if conf_vars['progresstype'].capitalize() == "Remainder": print(f"Duration: {current_api_info['duration']} / {current_api_info['progress']}")
		else: print(f"Duration: {current_api_info['progress']} / {current_api_info['duration']}")
		
		if current_api_info['explicit']: print("Explicit Content: Yes")
		else: print("Explicit Content: No")
		
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
		
		print("Song ID: " + current_track_id) 
		
		print(f"Status Modified At: {datetime.fromtimestamp(current_api_info['clock'] / 1000).strftime('%m-%d-%Y @ %X')}")

		#do not touch this please
		sleep(int(conf_vars['sleeptime']))
	except KeyboardInterrupt:
		log.SaveDiagInfo("Main - TL KeyboardInterrupt", "Pause Variable set to True", diaglog)
		toBePaused = True
	except RecursionError:
		log.SaveDiagInfo("Main - Recursion Catch", "Closing Program", diaglog)
		quit(69)
	#except:
	#	print("Catch-All+ Error")



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
		if toBePaused:
			log.SaveDiagInfo("toBePaused [Pause State: On]", "Pause Initiated", diaglog)
			clearTitle(f"Idle - Spotipy Current Song Info v.{conf_vars['version_no']}")
			print("SCSI is paused.")
			try:
				print(f"Last Song: {current_api_info['track_name']} by {current_api_info['artists']}\nAlbum: {current_api_info['album']}")
			except:
				print("Last Song: -----\nAlbum: -----")
			print("Press CTRL + C to unpause.\n")
			print(f"S.C.S.I version {conf_vars['version_no']}, python ver {platform.python_version()}")
			try:
				while True:
					sleep(1000)
			except KeyboardInterrupt:
				toBePaused = False
				try:
					log.SaveDiagInfo("toBePaused [Pause State: Waiting...]", "Resuming Program.", diaglog)
					clearTitle("Resuming...")
					print("Resuming program in 5 seconds.")
					print("Press CTRL + C again to close the program.")
					sleep(5)
					log.SaveDiagInfo("toBePaused [Pause State: Off]", "Pause Off.", diaglog)
				except KeyboardInterrupt:
					log.SaveDiagInfo("toBePaused [Exiting Program]", "Program Stopping...", diaglog)
					clearTitle("Stopping...")
					print("Stopping...")
					quit()

