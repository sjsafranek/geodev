import json


config = {}
with open('config.json', 'r') as fh:
	config = json.load(fh)


DATABASE = config['database']
DATA_DIRECTORY = config['app']['data_directory']