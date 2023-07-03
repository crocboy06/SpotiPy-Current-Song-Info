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
def errorfinder():
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
			sleep(timout2)
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