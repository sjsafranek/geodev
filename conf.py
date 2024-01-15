import json
from database import database as db


config = {}
with open('config.json', 'r') as fh:
	config = json.load(fh)


DATABASE = config['database']
DATA_DIRECTORY = config['app']['data_directory']


def get_credential(name):
	with db.open() as conn:
		cursor = conn.cursor()
		cursor.execute('''SELECT data FROM credentials WHERE name = %s;''', (name,))
		return cursor.fetchone()[0]
