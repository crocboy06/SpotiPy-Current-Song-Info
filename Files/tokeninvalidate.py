from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("config.ini")
conf_vars = config_object["CONFVARS"]
conf_vars['access_token'] = "INVALID"
with open('config.ini', 'w') as conf:
    config_object.write(conf)