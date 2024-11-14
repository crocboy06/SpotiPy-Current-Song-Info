def get_player_info(access_token):
	global response, toBePaused
	try:
		response = requests.get(
		conf_vars['api_link'],
		headers={
			"Authorization": f"Bearer {access_token}"},
		timeout=10)
	except requests.ReadTimeout:
		log.SaveDiagInfo("get_player_info [requests.ReadTimeout]", "None", diaglog)
		clearTitle("Read Timeout")
		print("We didn't recieve a response from Spotify.")
		print("There's nothing you can do, just sit tight.")
		print("Retrying in 5 seconds.")
		sleep(5)
		main()
	except requests.ConnectTimeout:
		log.SaveDiagInfo("get_player_info [requests.ConnectTimeout]", "None", diaglog)
		clearTitle("Connection Timeout")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		main()
	except requests.ConnectionError:
		log.SaveDiagInfo("get_player_info [requests.ConnectionError]", "None", diaglog)
		clearTitle("Connection Error")
		print("A connection-related request error has occured.")
		print("Retrying in 5 seconds.")
		print("Tip: Make sure your Wi-Fi/Ethernet is connected, with internet access.")
		sleep(5)
		main()
	except RecursionError:
		log.SaveDiagInfo("get_player_info [RecursionError]", "Except: Recursion Error", diaglog)
		quit()
	except KeyboardInterrupt:
		log.SaveDiagInfo("get_player_info [KeyboardInterrupt]", "Pause Variable set to True", diaglog)
		toBePaused = True
	except:
		return "Other API Error"
	if response.status_code == 401:
		if response.json()['error']['message'] in valid_401_messages:
			return 401
		else:
			log.SaveDiagInfo("get_player_info [response.status_code]", response.json['error']['message'], diaglog)	
			quit()
	if response.status_code == 204:
		return 204
	if response.status_code != 200:
		try:
			log.SaveDiagInfo("get_player_info [response_code != 200]", response.json(), diaglog)
		except:
			log.SaveDiagInfo("get_player_info [response_code != 200]", "json response dump failed.", diaglog)
		return response.status_code	
	#code = response.status_code
	json_resp = response.json()
	try:
		if json_resp['context']['uri'] == "spotify:playlist:37i9dQZF1EYkqdzj48dyYq":
			if json_resp['item'] == None:
				return "spotifydj"
	except None:
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
		"item": item,
	}

	return current_api_info
	 