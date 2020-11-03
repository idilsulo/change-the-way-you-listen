import argparse

import configparser

def make_parser(development=True):
	
	config = configparser.ConfigParser()
	config.read('config.ini')

	if development:
		return config['DEV']
	else:
		return config['PROD']


