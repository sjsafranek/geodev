import time
import datetime
import psycopg2
from sqlalchemy import create_engine

import conf

dbname = conf.DATABASE['name']
dbhost = conf.DATABASE['host']
dbuser = conf.DATABASE['user']
dbpass = conf.DATABASE['pass']
dbport = conf.DATABASE['port']


conn = psycopg2.connect(database=dbname, host=dbhost, user=dbuser, password=dbpass, port=dbport)


_previousToken = 0

def expire_cache():
	global _previousToken
	token = int(time.time()/3600)
	if token != _previousToken:
		print("Purging expired cache data")
		with conn.cursor() as cursor:
			cursor.execute('''SELECT cache__expire_rows_func();''')
			conn.commit()
			_previousToken = token


def set(key, value, max_age=None):
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
	expire_cache()
	cursor = conn.cursor()
	cursor.execute('''SELECT value FROM cache WHERE key = %s;''', (key,))
	return cursor.fetchone()


# def insertWeatherGeoDataFrame(gdf):
# 	# engine = create_engine(db_connection_url, echo=True)
# 	engine = create_engine(db_connection_url)
# 	print(engine)
# 	gdf.to_postgis("weather", engine, schema='public', if_exists='append', chunksize=100, index=True, index_label='idx')
# 	# df = geopandas.read_postgis(sql, con) 
# 	# df = geopandas.GeoDataFrame.from_postgis(sql, con)

