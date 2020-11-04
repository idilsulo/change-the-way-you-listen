import configparser
import os 

def make_parser(development=True):
	
	config = configparser.ConfigParser()
	
	path = os.getcwd() 
	if development: path += '/config.ini'
	else: path += "/mysite/config.ini"

	config.read(path)

	if development:
		return config['DEV']
	else:
		return config['PROD']

