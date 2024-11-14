from exceptions import *
import requests
from datetime import datetime
from confighandler import ConfigHandler
temp = ConfigHandler()
conf_vars = temp.GetConfig()
def get_player_info(access_token):
	
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
		raise ResponseCodeInvalid
	#code = response.status_code
	json_resp = response.json()
	try:
		if json_resp['context']['uri'] == "spotify:playlist:37i9dQZF1EYkqdzj48dyYq":
			if json_resp['item'] == None:
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
	context = json_resp['context']['uri']
	item = json_resp['item']

	current_api_info = {
		"id": track_id,
		"track_name": track_name,
		"context": context,
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
		#"response_code": code,
		"item": item,
	}

	return current_api_info
access_token = conf_vars['access_token']
try:
	current_api_info = get_player_info(access_token)
	print(current_api_info)
except ConnectionBad:
	pass
except TimeoutError:
	pass
except ConnectionBad:
	pass
except ConnectionError:
	pass
except JsonResponseError:
	pass
except TokenExpired:
	print("Token Invalid.")
	from trv2 import TokenRefresherV2
	a = TokenRefresherV2()
	a.RefreshToken()
except NoTrack:
	print("No Track...")
except DJPlaying:
	print("Spotify DJ is talking...")
