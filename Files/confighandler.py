class ConfigHandler():
	def __init__(self) -> None:
		pass
	def GetConfig(self):
		from configparser import ConfigParser
		config_object = ConfigParser()
		config_object.read("config.ini")
		conf_vars = config_object["CONFVARS"]
		return conf_vars
	def SaveConfig(self, config):
		self.config = config
		from configparser import ConfigParser
		config_object = ConfigParser()
		config_object.read("config.ini")
		conf_vars = config_object["CONFVARS"]
		with open('config.ini', 'w') as conf:
			config_object.write(conf)