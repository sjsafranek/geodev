
from database import database as db


def get(datasource_id, z, x, y):
    with db.open() as conn:
        cursor = conn.cursor()
        query = '''SELECT tile, mime_type FROM tile_cache WHERE datasource_id = %s AND z = %s AND x = %s AND y = %s;'''
        args = (datasource_id, z, x, y, )
        cursor.execute(query, args)
        return cursor.fetchone()


def set(datasource_id, mime_type, z, x, y, tile):
    with db.open() as conn:
        cursor = conn.cursor()
        query = '''INSERT INTO tile_cache(datasource_id, mime_type, z, x, y, tile) VALUES (%s, %s, %s, %s, %s, %s);'''
        args = (datasource_id, mime_type, z, x, y, tile, )
        cursor.execute(query, args)
        conn.commit()
