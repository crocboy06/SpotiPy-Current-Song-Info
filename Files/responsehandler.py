class handle_response():
	def __init__(self) -> None:
		pass
	def format_response(self, player_info):
		self.player_info = player_info
		if player_info['explicit']:
			player_info['explicit'] = "Yes"
		else:
			player_info['explicit'] = "No"
		if player_info['release_date_precision'] != "day":
			player_info['release_date'] += "(Imprecise)"
	def nuance_response(self, player_info):
		self.player_info = player_info
		return player_info
	def validity_checker(api_info):
		print("DEBUG PRINT 11")
		time.sleep(1204)
		apiInfo = api_info
		validity = {
				"valid_state": False,
				"reason": "n/a",
				"efcode": 000,
				"response_code": 000,
				"is_dj": False,
				"timestamp": "Valid",
				"id": "Valid",
				"type": "Valid",
		}
		response_code = api_info['response_code']
		validity['response_code'] = response_code #ALWAYS PASS BACK AN INTEGER FOR THIS
		validity['efcode'] = response_code #Integer or string alright here though
		#This check passed.

		if response_code != 200:
			validity['valid_state'] = False
			match response_code:
				case 429:
					validity['reason'] = "Rate Limit Exceeded"
				case 401:
					validity['reason'] = "Access Token Invalid"
				case 204:
					validity['reason'] = "No Content (No song playing)"
				case 403:
					validity['reason'] = "Bad OAuth Request"
				case _:
					validity['reason'] = f"Unknown: {response_code}"
		#This Check passed.
		if response_code == 200:
			validity['valid_state'] = True
			try: #This will not work because we do not pass back context. (Now we do, but verify functionality.)
				if apiInfo['context'] == "spotify:playlist:37i9dQZF1EYkqdzj48dyYq": #Verify this doesn't throw "NoneType not subscriptable."
					if apiInfo['item'] == None:
						validity['is_dj'] = True
			except:
				validity['is_dj'] = "Error"
			print("DEBUG PRINT 12")
			import time
			time.sleep(813)
			#Check 3 stopped here.
			try:
				if apiInfo['currently_playing_type'] != "track":
					print("TYPE NOT TRACK")
					validity['valid_state'] = False
					validity['reason'] = "Currently Playing Type invalid."
					validity['efcode'] = "CPT"
				else:
					validity['valid_state'] = True
					print("Type is Track")
			except:
				validity['valid_state'] = True
			try:
				if apiInfo['timestamp'] == "0" or 0:
					validity['timestamp'] = "Invalid"
			except:
				pass
			
			try:
				if apiInfo['item']['id'] == None:
					validity['id'] = "Invalid"
			except:
				pass
		#This Check Passed
		return validity