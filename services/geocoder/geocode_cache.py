from database import database as db


def set(key, source, rtype, value):
	with db.open() as conn:
		cursor = conn.cursor()
		query = '''INSERT INTO geocodes(id, source, type, value) VALUES (%s, %s, %s, %s);'''
		args = (key, source, rtype, value, )
		cursor.execute(query, args)
		conn.commit()


def get(key):
	with db.open() as conn:
		cursor = conn.cursor()
		cursor.execute('''SELECT value FROM geocodes WHERE id = %s;''', (key,))
		return cursor.fetchone()

