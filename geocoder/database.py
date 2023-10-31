import time
import datetime
import psycopg2

import conf

dbname = conf.DATABASE['name']
dbhost = conf.DATABASE['host']
dbuser = conf.DATABASE['user']
dbpass = conf.DATABASE['pass']
dbport = conf.DATABASE['port']
db_connection_url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(dbuser, dbpass, dbhost, dbport, dbname)


conn = psycopg2.connect(database=dbname, host=dbhost, user=dbuser, password=dbpass, port=dbport)


def set(key, source, rtype, value):
	cursor = conn.cursor()
	query = '''INSERT INTO geocodes(id, source, type, value) VALUES (%s, %s, %s, %s);'''
	args = (key, source, rtype, value, )
	cursor.execute(query, args)
	conn.commit()


def get(key):
	cursor = conn.cursor()
	cursor.execute('''SELECT value FROM geocodes WHERE id = %s;''', (key,))
	return cursor.fetchone()

