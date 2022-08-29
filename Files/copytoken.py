import pyperclip
Token = open('settings.txt', "r")
Token.seek(0)
ACCESS_TOKEN = Token.read()
Token.close
pyperclip.copy(ACCESS_TOKEN)