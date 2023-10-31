import json


config = {}
with open('config.json', 'r') as fh:
	config = json.load(fh)


DATABASE = config['database']