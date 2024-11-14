class APIHandler():
	def __init__(self):
		pass
	def SkipSong(self, token):
		import requests
		self.token = token
		skipURL = "https://api.spotify.com/v1/me/player/next"
		response = requests.post(
			skipURL,
			headers={"Authorization": f"Bearer {self.token}"},
			timeout=10
		)
		if response.status_code != 200:
			return "Error"
	def QueueTrack(self, token, songID, deviceID):
		import requests
		self.songID = songID
		self.deviceID = deviceID
		self.token = token
		track = f"spotify:track:{songID}"
		track.replace(":", "%3A")
		queueURL = f"https://api.spotify.com/v1/me/player/queue?uri={track}"
		#postUrl = queueURL + f"&deviceid={deviceID}"
		response = requests.post(
			queueURL,
			headers={"Authorization": f"Bearer {token}"},
			timeout=10
		)
		return response.status_code
	def LoopTrack(self, token, deviceID):
		import requests
		self.token = token
		self.deviceID = deviceID
		loopPostURL = "https://api.spotify.com/v1/me/player/repeat?state=track" + f"&deviceid={deviceID}"
		response = requests.put(
			loopPostURL,
			headers={"Authorization": f"Bearer {token}"},
			timeout=10
		)