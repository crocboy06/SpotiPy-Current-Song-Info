#credit to bingbong for that 204 error help
#stealing my code is really lame, so don't do that

#CODE GRAVEYARD
#Stuff getting removed soon
#---------------------START GRAVEYARD---------------------


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
global json_resp, last_track_id, access_token, title, current_api_info, response, lines, starttimestamp
global char

starttimestamp = str(datetime.fromtimestamp(datetime.now().timestamp()).strftime("%m-%d-%Y, %H-%M-%S"))
songlog = open("logs/" + starttimestamp + ".txt", "w+")
songlog.write("SONG LOG FOR SESSION | " + starttimestamp)
songlog.close()


#place BADASS OOP stuff here
class eventlogger():
	def __init__(self):
		pass
	def logEvent(self, event, adtl_details):
		self.event = event

		self.details = adtl_details
		logg = open('logs/' + starttimestamp + ".txt", "a")
		logg.write(f"\nRecorded Event @ {datetime.now().strftime('%H:%M:%S')}")
		logg.write(f"\n{self.event}")
		logg.write(f"\nAdditional Details: {self.details}\n")
		logg.close()
class songlogger():
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
last_track_id = None
config_object = ConfigParser()
config_object.read("config.ini")
conf_vars = config_object["CONFVARS"]
access_token = conf_vars['access_token']
title = ""
char = ""
eligibility = ""
log = eventlogger()

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
	"4UoDSs5VAw6xHdzbkjocTM": 'os.system("title THEY SAY THEY WANNA READ MY MIND 🔊🔊🔊")',
	"3QzAOrNlsabgbMwlZt7TAY": 'os.system("title Axel in Harlem by Animan Studios")',
	"6E1YebXpPPtujMUljDNlOo": 'os.system("title Audi RS6 300km/h")',
	}

#Place functions here

def tokenrefresher():
	log = eventlogger()
	log.logEvent("Token Refresher Started", "wait for refresh status...")
	global access_token
	global conf_vars
	try:
		import trv2
		trv2		
		config_object = ConfigParser()
		config_object.read("config.ini")
		conf_vars = config_object["CONFVARS"]
		access_token = conf_vars['access_token']
		with open('config.ini', 'w') as conf:
			config_object.write(conf)
		log.logEvent("Token Refresher: Success", "No exceptions thrown | TRV2")
	except:
		log.logEvent("Token Refresher: Unsuccessful", "Reverting to Backup flask method.")
		keyboard = Controller()
		timeout_s = 3  # how many seconds to wait 
		try:
			webbrowser.open("http://localhost:5000")
			p = subprocess.run("flask run", timeout=timeout_s)
			log.logEvent("Token Refresh: Web Browser", "Web Browser opened, subprocess running...")
		except subprocess.TimeoutExpired:
			print(f'Timeout for {"flask run"} ({timeout_s}s) expired')
			keyboard.press(Key.ctrl)
			keyboard.press(W)
			keyboard.release(Key.ctrl)
			keyboard.release(W)
			log.logEvent("Token Refresher: Complete", "Process Complete. (Backup method)")
	config_object = ConfigParser()
	config_object.read("config.ini")
	conf_vars = config_object["CONFVARS"]
	access_token = conf_vars['access_token']
	with open('config.ini', 'w') as conf:
		config_object.write(conf)
	
	os.system("cls")

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
	global access_token
	log = eventlogger()
	try:
		if json_resp['timestamp'] == 0:
			log.logEvent("Error Finder: Timestamp 0", "Timestamp ignored, re-acquiring info")
			main()
	except:
		clearTitle("Error")
		print("We've encountered an error.")
		log.logEvent("Error Finder: API Response", f"Code= {json_resp['error']['status']}, API Info: {json_resp['error']['message']}")
		print(f"The Error code we recieved is: {json_resp['error']['status']}")
		print(f"Additional information: {json_resp['error']['message']}")
		match json_resp['error']['status']:
			case 429:
				if int(conf_vars['sleeptime']) > 5:
					log.logEvent("Error Finder: 429/Rate Limit", "Program Halted, Sleeptime excessive.")
					clearTitle("Rate Limit Stop")
					print("Repeated API Rate limit errors, please refresh your token, and try again later.")
					quit()
				slt = int(conf_vars['sleeptime']) + 1
				conf_vars['sleeptime'] = str(slt)
				log.logEvent("Error Finder: 429/Sleeptime", "Sleeptime Increased.")
				with open('config.ini', 'w') as conf:
					config_object.write(conf)
			case 401:
				tokenrefresher()
				access_token = conf_vars['access_token']
				log.logEvent("Function401", "Refreshed (Line 185)")

def errorfinder():
	global access_token
	match current_api_info:
		case 204:
			clearTitle("Idle - SpotiPy Current Song Info")
			print("There is currently no music playing.\n")
			print("SpotiPy Current Song Info")
			print(f"Ver {conf_vars['version_no']}")
			if conf_vars['deep_idle'].capitalize() == "True": print("Deep Idle Enabled. API Requests limited to once every 30 seconds.")
			print("Waiting for music to play.")
			if conf_vars['deep_idle'].upper() == "TRUE": timeout2 = 30 
			else: timeout2 = 5
			sleep(timeout2)
		case 429:
			if int(conf_vars['sleeptime']) > 5:
				log.logEvent("MatchAPIinfo", "Program stopping, Sleeptime too much.")
				clearTitle("Rate Limit Stop")
				print("Repeated API Rate limit errors, please refresh your token, and try again later.")
				quit()
			slt = int(conf_vars['sleeptime']) + 1 
			conf_vars['sleeptime'] = str(slt)
			log.logEvent("MatchAPIinfo: Rate Limit", "Sleeptime Increased.")
			with open('config.ini', 'w') as conf:
				config_object.write(conf)
			sleep(5)
		case 401:
			tokenrefresher()
			access_token = conf_vars['access_token']
			log.logEvent("Function401", "Refreshed (Line 185)")
		case 403:
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
			clearTitle("Access Token Expired?")
			log.logEvent("Get_Api_information/Case401", response.json() )
			log.logEvent("Get_Api_Information/Case401", "Calling Token Refresher")
			match response.json()['error']['message']:
				case "The access token expired":
					log.logEvent("MatchAPIinfo/Refresh Reason", "Token Expiration")
				case "Invalid access token":
					log.logEvent("MatchAPIinfo/Refresh Reason", "The token was invalid")
				case _:
					log.logEvent("MatchAPIinfo/Refresh Reason", "Unknown")
			try:
				tokenrefresher()
				access_token = conf_vars['access_token']
			except: 
				log.logEvent("GET_API_INFORMATION LN306", "Refresh Failed, Stopping")
				quit(401)
			access_token = conf_vars['access_token']
			main()

		case "timestamp 0":
			log.logEvent("MatchAPIinfo", "Timestamp Invalid")
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
			print("Unknown API error encountered.\nRetrying in 5 seconds.")
			sleep(5)
			main()
		case "other json_resp error":
			clearTitle("Other JSON_RESP Error")
			print("There was an unknown error with the JSON Response.")
			print("Retrying in 5 seconds.")
			sleep(5)
			main()
		case "currently_playing_type error":
			clearTitle("Error")
			print("The currently playing type ID was invalid.")
			print("Retrying in 5 seconds.")
			sleep(5)
			main()

def get_api_information(access_token):
	log = eventlogger()
	try:
		response = requests.get(
		conf_vars['api_link'],
		headers={
			"Authorization": f"Bearer {conf_vars['access_token']}"},
		timeout=10)
	except requests.ReadTimeout:
		clearTitle("Read Timeout")
		print("Spotify's API failed to reply within 10 seconds.")
		print("Retrying in 5 seconds.")
		log.logEvent("API Info: Read Timeout", "None")
		sleep(5)
		main()
	except requests.ConnectTimeout:
		log.logEvent("Connection Timeout", "None")
		clearTitle("Connection Timeout")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		main()
	except requests.ConnectionError:
		clearTitle("Connection Error")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		main()
	except RecursionError:
		log.logEvent("Recursion Error", "Right under all the except requests catchers")
		quit()
	except:
		return "Other API Error"
		
	if response.status_code != 200:
		return response.status_code
			
	#global json_resp
	json_resp = response.json()

	try:
		if json_resp['currently_playing_type'] != "track":
			return json_resp['currently_playing_type']
	except:
		return "currently playing type error"
	#errorfinder()
	if json_resp['timestamp'] == "0" or 0:
		return "timestamp 0"
	try:
		if json_resp['item']['id'] == None:
			return "no id"
	except:
		if json_resp['context']['uri'] == "spotify:playlist:37i9dQZF1EYkqdzj48dyYq":
			return "dj playing"
		else:
			return "other json_resp error"
	
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
						print("Play a new song to prevent loop.")
						print("Returning to normal in 10 seconds...")
						sleep(10)

def lamemusic():
	global conf_vars
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
	log = eventlogger()
	try:
		try:
			current_api_info = get_api_information(access_token)
			errorfinder()
		except:
			os.system("cls")
			os.system("title Error")
			print("There was an error while trying to get API Information.")
			print("Attempting to resume in 3 seconds.")
			sleep(3)
			main() 
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

		if current_api_info['albumtype'] == "album": print(f"Album: {current_api_info['album']} | Track {current_api_info['track_no']}")
		if current_api_info['albumtype'] != "album": print(f"Album: {current_api_info['album']} [{current_api_info['albumtype'].capitalize()}]")
		
		if conf_vars['progresstype'] == "Remainder": print(f"Duration: {current_api_info['duration']} / {current_api_info['progress']}")
		if conf_vars['progresstype'] != "Remainder": print(f"Duration: {current_api_info['progress']} / {current_api_info['duration']}")
	
		if current_api_info['explicit']: print("Explicit: Yes")
		if not current_api_info['explicit']: print("Explicit: No")
		
		if current_api_info['release_precision'] != "day": print(f"Released: {current_api_info['release_date']} (Imprecise) | Eligible: {eligibility}")
		if current_api_info['release_precision'] == "day": print(f"Released: {current_api_info['release_date']} | Eligible: {eligibility}")
		
		if conf_vars['tracklink'] == "True": print(f"Play it Here: {current_api_info['link']}")
		
		print("TrackID: " + current_track_id) 
		print(f"Last Song Change: {datetime.fromtimestamp(current_api_info['clock'] / 1000).strftime('%m-%d-%Y @ %X')}")
		
		
		#do not touch this please
		sleep(int(conf_vars['sleeptime']))
	except KeyboardInterrupt:
		try:
			os.system('cls')
			os.system(f"title Paused - SpotiPy Current Song Info v{conf_vars['version_no']}")
			log.logEvent("Main: CTRL+C", "Program Paused.")
			print(f"Last Song: {current_api_info['track_name']} by {current_api_info['artists']}\nAlbum: {current_api_info['album']}")
			print("Press CTRL + C to Resume.")
			while True:
				time.sleep(10000)
		except KeyboardInterrupt:
			try:
				log.logEvent("Main: CTRL+C", "Resuming Function.")
				os.system('cls')
				os.system("title Resuming...")
				print("Resuming program in 5 seconds.")
				sleep(5)
			except KeyboardInterrupt:
				log.logEvent("Main: CTRL+C", "Program Terminated.")
				os.system("cls")
				print("SCSI Stopped")
				print("Reason: KeyboardInterrupt")
				print(f"SCSI v{conf_vars['version_no']}")
				exit("-----Program Terminated-----")
	except:
		clearTitle("Error")
		print("Error encountered while running main()")
		log.logEvent("Main/Highest level except", "Correcting")
		main()



cursor.hide()
log.logEvent("Highest Level: Cursor", "Cursor Hidden")
#migrated all ACCESS_TOKEN to lowercase

#it is needed


if conf_vars['logging'] == "True":
	print("Logging Enabled")
	
def for_uhh_ever():
	main()

if __name__ == '__main__': 
	lines = 12
	if conf_vars['tracklink'] == "False": os.system(f"mode con cols=70 lines={str(lines)}")
	else: 
		lines += 1
		os.system(f"mode con cols=70 lines={lines}")
	while True:
		for_uhh_ever()

