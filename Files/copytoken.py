import configparser
from distutils.command.config import config
import pyperclip
from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("config.ini")
conf_vars = config_object["CONFVARS"]

access_token = conf_vars['access_token']
pyperclip.copy(access_token)