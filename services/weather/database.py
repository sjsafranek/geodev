import time
import datetime

from database import database as db


_previousToken = 0


def expire_cache(conn):
	global _previousToken
	token = int(time.time()/3600)
	if token != _previousToken:
		print("Purging expired cache data")
		with conn.cursor() as cursor:
			cursor.execute('''SELECT cache__expire_rows_func();''')
			conn.commit()
			_previousToken = token


def set(key, value, max_age=None):
	with db.open() as conn:
		cursor = conn.cursor()
		query = '''INSERT INTO cache(key, value) VALUES (%s, %s);'''
		args = (key, value, );
		if max_age:
			now = datetime.datetime.now()
			query = '''INSERT INTO cache(key, value, expires_at) VALUES (%s, %s, %s);'''
			args = (key, value, now+max_age, )
		cursor.execute(query, args)
		conn.commit()


def get(key):
	with db.open() as conn:
		expire_cache(conn)
		cursor = conn.cursor()
		cursor.execute('''SELECT value FROM cache WHERE key = %s;''', (key,))
		return cursor.fetchone()

