class LogFunc():
	def __init__(self):
		pass
	def SaveSongInfo(self, name, artist, id, LogName):
		self.name = name
		self.artist = artist
		self.id = id
		self.LogName = LogName
		songlog = open('logs/songlogs/' + self.LogName + ".txt", "a")
		songlog.write("\n-----------------------------------\n")
		songlog.write("Track: " + self.name +'\n')
		songlog.write("Artist: " + self.artist +'\n')
		songlog.write("ID: " + self.id +'\n')
		songlog.write("-----------------------------------")
		songlog.close()
	def SaveDiagInfo(self, event, adtl_details, LogName):
		from datetime import datetime
		self.event = event
		self.details = adtl_details
		self.LogName = LogName
		logg = open('logs/diagnostics/' + self.LogName + ".txt", "a")
		logg.write(f"\nEvent @ {datetime.now().strftime('%H:%M:%S')} | {self.event}")
		logg.write(f"\nAdditional Details: {self.details}\n")
		logg.close()

class logFileCreator():
	def __init__(self):
		pass
	def createLog(self, LogType):
		from datetime import datetime
		import platform
		self.LogType = LogType
		logName = str(datetime.fromtimestamp(datetime.now().timestamp()).strftime('%m-%d-%Y, %H-%M-%S'))
		match self.LogType:
			case "diagnostic":
				creator = open(f"logs/diagnostics/{logName}.txt", "w+")
				creator.write(f"Diagnostics for {logName}, Python Ver. {platform.python_version()}")
			case "song":
				creator = open(f"logs/songlogs/{logName}.txt", "w+")
				creator.write(f"Song Log for {logName}")
		creator.close()
		return logName
	
#debug
if __name__ == "__main__":
	a = input("Create Log? Y/N")
	if a == "Y":
		b = logFileCreator()
		c = b.createLog("diagnostic")
		d = b.createLog("song")
		print(f"Diagnostic Log created. Name: {c}")
		print(f"Song Log created. Name: {d}")