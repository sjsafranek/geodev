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


def fetchall():
	cursor = conn.cursor()
	cursor.execute('''
SELECT json_agg(c)
	FROM (
		SELECT* FROM datasource
) c;''')
	return cursor.fetchone()[0]



def fetch(datasource_id: str):
	datasources = [ds for ds in fetchall() if ds['id'] == datasource_id]
	if 0 == len(datasources):
		return None
	return datasources[0]