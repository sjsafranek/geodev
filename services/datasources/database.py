from database import database as db


def fetchall():
	with db.open() as conn:
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
