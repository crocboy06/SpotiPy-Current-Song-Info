#credit to bingbong for that 204 error help
#stealing my code is really lame, so don't do that

#CODE GRAVEYARD
#Stuff getting removed soon
#---------------------START GRAVEYARD---------------------
#errors = ErrorChecker


#---------------------END GRAVEYARD---------------------

from distutils.command.config import config
from re import A
import cursor, json, requests, time, os, subprocess, pyperclip, pynput, webbrowser
from pynput import keyboard
from pynput.keyboard import Key, Controller
from datetime import datetime
from time import sleep
from configparser import ConfigParser
from tkinter import W
global conf_vars
global json_resp, last_track_id, access_token, title, current_api_info, response, lines
global char
#place BADASS OOP stuff here
class songlogger():
	global starttimestamp
	def __init__(self, name, artist, id):
		self.name = name
		self.artist = artist
		self.id = id
	def saveInfo(self):
		print("To Be Saved:")
		songlog = open('logs/' + starttimestamp + ".txt", "a")
		songlog.write("\n-----------------------------------\n")
		songlog.write("Track: " + self.name +'\n')
		songlog.write("Artist: " + self.artist +'\n')
		songlog.write("id: " + self.id +'\n')
		songlog.write("-----------------------------------")
		songlog.close()
#vars
config_object = ConfigParser()
config_object.read("config.ini")
conf_vars = config_object["CONFVARS"]
access_token = conf_vars['access_token']
title = ""
char = ""
eligibility = ""

#dictionaries
forbidden_dict = {
	"(": 'title.replace("(","[OpPr]")',
	")": 'title.replace(")","[ClPr]")',
	"<": 'title.replace("<","[LsThn]")',
	">": 'title.replace(">","[GrThn]")',
	"^": 'title.replace("^","Pwr")',
	"|": 'title.replace("|","[VBar]")',
	"&": 'title.replace("&","and")',
}

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
	"6o0IPNoi3PZi9tkoyVGXSB": 'os.system("title IM DA BIGGEST BURD IM DA BIGGEST BURD")',
	"2iJuuzV8P9Yz0VSurttIV5": 'os.system("title iam+ PHOTO SOCIAL")',
	"4Li2WHPkuyCdtmokzW2007": 'os.system("title Remind me, Who was in Paris?")',
	"373gDROnujxNTFa1FojYIl": 'os.system("title Numb (Pt. 2) by Linkin Park")',
	"4UoDSs5VAw6xHdzbkjocTM": 'os.system("title THEY SAY THEY WANNA READ MY MIND 🔊🔊🔊")'
	}

#Place functions here

def tokenrefresher():
	global access_token
	global conf_vars
	try:
		import trv2
		trv2
	except:
		keyboard = Controller()
		timeout_s = 3  # how many seconds to wait 
		try:
			webbrowser.open("http://localhost:5000")
			p = subprocess.run("flask run", timeout=timeout_s)
		except subprocess.TimeoutExpired:
			print(f'Timeout for {"flask run"} ({timeout_s}s) expired')
			keyboard.press(Key.ctrl)
			keyboard.press(W)
			keyboard.release(Key.ctrl)
			keyboard.release(W)
	config_object = ConfigParser()
	config_object.read("config.ini")
	conf_vars = config_object["CONFVARS"]
	access_token = conf_vars['access_token']
	
	os.system("cls")
	print("Access Token refreshed successfully.")

def errorfinder():
	global access_token
	try:
		#This was implemented to prevent "NoneType is not subscriptable" TypeError.
		#This error was found to occur when the program calls to the API to try and get current song information while the user is inbetween songs.
		#Most likely the inbetween period is over, so lets get song information after we wait 5 seconds
		if json_resp['timestamp'] == 0:
			if not conf_vars['silenterrors']:
				os.system("cls")
				os.system("title " + "Error")
				print("Whoops! You caught us at a bad time.")
				print("Something's gone wrong.")
				print("We'll retry this in 5 seconds.")
				if conf_vars['debuginfo']: print("Error Code: TIMESTAMP_EQUAL_TO_ZERO")
				if conf_vars['extended_debug_info']: print("Most common cause is that the user is inbetween songs.")
				sleep(5)
				#Once the error has been handled, and the user knows, refresh the current song and get a new JSON response to clear the error
			get_api_information(access_token)
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
				#API Rate print removed. Tis gay and unneccesary
				if int(conf_vars['sleeptime']) > 5:
					os.system("cls")
					print("Repeated API Rate limit errors, please refresh your token, and try again later.")
					quit()
				slt = int(conf_vars['sleeptime'])
				slt += 1
				conf_vars['sleeptime'] = str(slt)
				with open('config.ini', 'w') as conf:
					config_object.write(conf)
			case 401: #FIX THIS RIGHT NEOOWWWW
				os.system('cls')
				os.system('title Error')
				def Function401():
					tokenrefresher()
					response = requests.get(
						conf_vars['api_link'],
						headers={
							"Authorization": f"Bearer {conf_vars['access_token']}"},
						timeout=10)
					match response.status_code:
						case 401:
							print("We are unable to fix the error automatically")
							print("Error Reference '401 refresh failed'")
							print("Closing Automatically in 10 Seconds.")
							sleep(10)
							quit()
						case 429:
							sleep(10)
						case 200:
							pass
						case _:
							quit()
							
									
					get_api_information(access_token)
				Function401()

def get_api_information(access_token):
	try:
		response = requests.get(
		conf_vars['api_link'],
		headers={
			"Authorization": f"Bearer {conf_vars['access_token']}"},
		timeout=10)
	except requests.ReadTimeout:
		os.system('cls')
		if conf_vars['silenterrors'].lower() == "false":
			os.system('cls')
			os.system("title TIMEOUT")
			print("Spotify's API failed to reply within 10 seconds.")
			print("Retrying in 5 seconds.")
		sleep(5)
		get_api_information(access_token)
	except requests.ConnectTimeout:
		os.system('cls')
		os.system("title Connection Error")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		get_api_information(access_token)
	except requests.ConnectionError:
		os.system('cls')
		os.system("title Connection Error")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		get_api_information(access_token)
	except:
		os.system('cls')
		os.system("title Unknown Error")
		print("We've encountered an error that we don't have a fix for.")
		try:
			print(f"The API Response code was: {response.status_code}")
			print("Write that down, and implement it into the program.")
		except:
			print("The API Response code was unable to be retrieved.")
		print("Retrying in 5 seconds.")
		try:
			get_api_information(access_token)
		except RecursionError:
			os.system('cls')
			os.system("title Recursion Max Depth Reached.")
			print("You've run the program so long that you've hit a recursion error")
			print("Re-Launch the program to fix this issue.")
			quit()
		except:
			os.system('cls')
			os.system('title critical STOP')
			print(f"Check Call Stack in Debugging mode for more details.\nQuitting Program")
	match response.status_code:
			case 204:
				while response.status_code == 204:
					os.system("cls")
					os.system("title Nothing Playing")
					print("There is currently no music playing.\n")
					print("SpotiPy Current Song Info.")
					print(f"Ver {conf_vars['version_no']}")
					print("Waiting for music to play...")
					try:
						response = requests.get(
						conf_vars['api_link'],
						headers={
							"Authorization": f"Bearer {conf_vars['access_token']}"},
						timeout=10)
						sleep(1)
					except requests.ReadTimeout:
						os.system('cls')
						os.system('title Debug//Nothing Playing')
						print("timeout exceeded nothing returned")
						sleep(10)
			case 403:  
				os.system('cls')
				os.system('title Uncommon Error')
				print("For some reason, we're forbidden from getting API information")
				print("Check the API link in config.ini")
				print("MAKE SURE: The market on your api link matches your reigon. ex: US=ES")
				print("MAKE SURE: User is authorized in spotify developer portal")
				print("It should be linked to spotify's API under the \'player\' category")
				print("Unfortunately, this isn't something the program can fix automatically")
				print("The program will close in 5 seconds.")
				sleep(5)
				quit()
			case 401:
				os.system('cls')
				os.system('title Token Expired')
				os.system("title Refreshing Token...")
				os.system("cls")
				tokenrefresher()
				access_token = conf_vars['access_token']
				get_api_information(access_token)
			case 200:
				pass
			case _:
				os.system('cls')
				os.system('title API Response code error')
				print(f"Given API Response code:{response.status_code}")
				sleep(10)

#	try:
#		if response.status_code == 204:
#			pass
#	except:
#		get_api_information(access_token)
	
	global json_resp
	json_resp = response.json()


	errorfinder()
	match json_resp["currently_playing_type"]:
		case "ad":
			os.system("cls")
			os.system("title Advertisement")
			print("Advertisement")
			print("Upgrade to Spotify Premium to remove advertisements.")
			print("SCSI will be back shortly.")
			print(f"\nSpotiPy Current Song Info v{conf_vars['version_no']}")
			sleep(1)
			get_api_information(access_token)
		case "podcast":
			os.system("cls")
			os.system("title Podcast")
			print("We do not support podcasts.")
			print("Play a song, and we'll get things rolling")
			sleep(5)
			get_api_information(access_token)
		case "episode":
			os.system("cls")
			os.system("title Podcast")
			print("We do not support podcasts.")
			print("Play a song, and we'll get things rolling")
			sleep(5)
			get_api_information(access_token)
	if json_resp['timestamp'] == "0":
		print("timestamp error (should never be seen)")
		sleep(1123)
	try:
		if json_resp['item']['id'] == None:
			os.system('cls')
			os.system("title JSON Response Error")
			print("JSON_RESP Error")
			print(json_resp)
			print("Retrying in 5 seconds.")
			sleep(15)
			get_api_information(access_token)
	except:
		os.system('cls')
		os.system('title JSON Response Error')
		print("JSON_RESP Error")
		print("This can be caused by Spotify's new DJ feature.")
		print("Retrying in 5 seconds.")
		sleep(5)
		get_api_information(access_token)
	if json_resp['timestamp'] == "0":
		print("timestamp error (should never be seen)")
		sleep(1123)
	
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
	devtype = json_resp['device']['type']
	devid = json_resp['device']['id']
	releaseDatePrecision = json_resp['item']['album']['release_date_precision']

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
						saveinfo = songlogger(current_api_info["track_name"], current_api_info['artists'], current_api_info['id'])
						saveinfo.saveInfo()
					os.system("shutdown -r /t 00")
				case "6LNoArVBBVZzUTUiAX2aKO":
					if conf_vars['logging'] == "True":
						songlog = open('logs/' + starttimestamp + ".txt", "a")
						saveinfo = songlogger(current_api_info["track_name"], current_api_info['artists'], current_api_info['id'])
						saveinfo.saveInfo()
						songlog.close()
					try:
						os.system("cls")
						os.system('title ------- SHUTDOWN IMMINENT -------')
						print("Stop shutdown by pressing CTRL + C in the next 10 seconds.")
						print("If the shutdown isn't aborted in that time, computer will shutdown.")
						print(f"SCSI v{conf_vars['version_no']}")
						sleep(10)
						os.system("shutdown -s /t 00")
					except KeyboardInterrupt:
						print("ABORTED SHUTDOWN")
						print("Play a new song to prevent loop")
						print("Returning to normal in 10 seconds...")
						sleep(10)
def mainSimple():
	global current_api_info
	current_api_info = get_api_information(access_token)
	if current_api_info['explicit']:
		os.system(f'title \"{current_api_info["track_name"]}\"[Explicit]')
	else:
		os.system(f'title \"{current_api_info["track_name"]}\"')
	os.system("cls")
	print("Artist(s): " + current_api_info['artists'])
	print("Song: " + current_api_info['track_name'])
	if current_api_info['albumtype'] != "album": 
		print("Album: " + current_api_info['album'] + ' [' + current_api_info['albumtype'].capitalize() + ']')
	else:
		print("Album: " + current_api_info['album'])
	if conf_vars['progresstype'] == "Remainder": print("Duration: " + current_api_info['duration'] + " / " + current_api_info['progress'])
	if conf_vars['progresstype'] != "Remainder": print("Duration: " + current_api_info['progress'] + " / " + current_api_info['duration'])
	sleep(int(conf_vars['sleeptime']))
def lamemusic():
	devid = current_api_info['devid']
	queueURL = "https://api.spotify.com/v1/me/player/queue?uri="
	skipURL = "https://api.spotify.com/v1/me/player/next"
	track = "spotify:track:55WLWX71YkHt2tSucNIf1g"
	postUrl = queueURL + track.replace(":", "%3A") + "&deviceid=" + devid
	loopPostURL = "https://api.spotify.com/v1/me/player/repeat?state=track" + "&device_id=" + devid
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
		os.system("cls")
		os.system("title Error whilst correcting your TERRIBLE music taste")
		print("Couldn't execute API calls for changing music.")
		print("Easter Eggs disabled for the rest of this session.")
		print("Continuing in 5 seconds.")
		sleep(5)
		conf_vars['eastereggs'] = "false"

def main():
	try:
		global current_api_info
		global last_track_id
		global eligibility
		try:
			current_api_info = get_api_information(access_token)
		except:
			os.system("cls")
			os.system("title Error")
			print("There was an error while trying to get API Information.")
			print("Attempting to resume in 3 seconds.")
			sleep(3)
			current_api_info = get_api_information(access_token)
		if conf_vars['eastereggs'].lower() == "true":
			try:
				if "Yameii Online" in current_api_info['artists']:
					lamemusic()
			except:
				print("Check for artist failed.")
		current_track_id = current_api_info['id']
		if current_track_id != last_track_id:
			if conf_vars['clipboard'] == "True": pyperclip.copy(current_api_info['track_name'] + " by " + current_api_info['artists'] + " | " +current_api_info['album'])
			eligibility_year = int(current_api_info['release_date'].split("-")[0])
			if 2000 <= eligibility_year < 2020:
				eligibility = "Yes"
			else:
				eligibility = "No"

		if conf_vars['logging'] == "True":
			if current_track_id != last_track_id:
				saveinfo = songlogger(current_api_info["track_name"], current_api_info['artists'], current_api_info['id'])
				saveinfo.saveInfo()
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
		
		match current_api_info['devtype']:
			case "Smartphone":
				try:
					print(f"Pb Device: {current_api_info['devicename']} (Smartphone) | {current_api_info['volume']}% Volume")
				except:
					print(f"Pb Device: Unavailable | Volume: Unavailable")
			case "Computer":
				try:
					print(f"Pb Device: {current_api_info['devicename']} (Computer) | {current_api_info['volume']}% Volume")
				except:
					print(f"Pb Device: Unavailable | Volume: Unavailable")
			case "Tablet":
				try:
					print(f"Pb Device: {current_api_info['devicename']} (Tablet) | {current_api_info['volume']}% Volume")
				except:
					print(f"Pb Device: Unavailable | Volume: Unavailable")
			case "Unknown":
				try:
					print(f"Pb Device: {current_api_info['devicename']} (Unknown) | {current_api_info['volume']}% Volume")
				except:
					print(f"Pb Device: Unavailable | Volume: Unavailable")

		if current_api_info['playing']: print("Pb Status: Playing") 
		if not current_api_info['playing']: print("Pb Status: Paused")
		
		print(f"Artist(s): {current_api_info['artists']}")
		print(f"Song: {current_api_info['track_name']}")

		if current_api_info['albumtype'] == "album": print(f"Album: {current_api_info['album']}")
		if current_api_info['albumtype'] != "album": print(f"Album: {current_api_info['album']} [{current_api_info['albumtype'].capitalize()}]")
		
		if conf_vars['progresstype'] == "Remainder": print(f"Duration: {current_api_info['duration']} / {current_api_info['progress']}")
		if conf_vars['progresstype'] != "Remainder": print(f"Duration: {current_api_info['progress']} / {current_api_info['duration']}")
	
		if current_api_info['explicit']: print("Explicit: Yes")
		if not current_api_info['explicit']: print("Explicit: No")
		
		if current_api_info['release_precision'] != "day": print(f"Released: {current_api_info['release_date']} (Imprecise) | Eligible: {eligibility}")
		if current_api_info['release_precision'] == "day": print(f"Released: {current_api_info['release_date']} | Eligible: {eligibility}")
		
		if conf_vars['tracklink'] == "True": print(f"Play it Here: {current_api_info['link']}")
		
		print("TrackID: " + current_track_id) 
		print(f"Last Song Change: {datetime.fromtimestamp(current_api_info['clock'] / 1000).strftime('%m-%d-%Y @ %H:%M:%S')}")
		
		
		#do not touch this please
		sleep(int(conf_vars['sleeptime']))
	except KeyboardInterrupt:
		try:
			os.system('cls')
			os.system("title Program Stopped.")
			print("CTRL + C Pressed, Program Paused.")
			print(f"Last Song: {current_api_info['track_name']} by {current_api_info['artists']}\nAlbum: {current_api_info['album']}")
			print("Press CTRL + C to resume function")
			while True:
				time.sleep(10000)
		except KeyboardInterrupt:
			try:
				os.system('cls')
				os.system("title Resuming...")
				print("Resuming program in 5 seconds.")
				sleep(5)
			except KeyboardInterrupt:
				os.system("cls")
				print("SCSI Stopped")
				print("Reason: KeyboardInterrupt")
				print(f"SCSI v{conf_vars['version_no']}")
				exit("-----Program Terminated-----")



cursor.hide()

#migrated all ACCESS_TOKEN to lowercase

#it is needed
last_track_id = None

if conf_vars['logging'] == "True":
	print("Logging Enabled")
	starttimestamp = str(datetime.fromtimestamp(datetime.now().timestamp()).strftime("%m-%d-%Y, %H-%M-%S"))
	songlog = open("logs/" + starttimestamp + ".txt", "w+")
	songlog.write("SONG LOG FOR SESSION | " + starttimestamp)
	songlog.close()

if __name__ == '__main__': 
	lines = 12
	match conf_vars['mode']:
		case "simple":
			os.system("mode con cols=70 lines=5")
			while True:
				mainSimple()

		case "default":
			if conf_vars['tracklink'] == "False": os.system(f"mode con cols=70 lines={str(lines)}")
			else: 
				lines += 1
				os.system(f"mode con cols=70 lines={lines}")
			while True:
				main()
		case _:
			if conf_vars['tracklink'] == "False": os.system(f"mode con cols=70 lines={str(lines)}")
			else: os.system(f"mode con cols=70 lines={lines}")
			while True:
				main()
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
