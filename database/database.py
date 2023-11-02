import psycopg2

import conf

dbname = conf.DATABASE['name']
dbhost = conf.DATABASE['host']
dbuser = conf.DATABASE['user']
dbpass = conf.DATABASE['pass']
dbport = conf.DATABASE['port']


def open():
	return psycopg2.connect(
		database=dbname, 
		host=dbhost, 
		user=dbuser, 
		password=dbpass, 
		port=dbport
	)


# def insert(query, args=None):
# 	with open() as conn:
# 		cursor = conn.cursor()
# 		cursor.execute(query, args)
# 		conn.commit()