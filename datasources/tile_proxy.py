import os.path
from urllib.parse import urlsplit

from datasources import tile_cache
from utils.HttpClient import HttpClient


CLIENTS = {}


Extension2MimeType = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'mvt': 'application/octet-stream',
    'protobuf': 'application/octet-stream'
}


def getExtentsionFromPath(path):
    return os.path.splitext(path)[-1]


def getMimeTypeFromPath(path):
    ext = getExtentsionFromPath(path)
    return Extension2MimeType.get(ext[1:])


def getClient(base_url):
    if base_url not in CLIENTS:
        CLIENTS[base_url] = HttpClient(base_url)
    return CLIENTS[base_url]


def fetch(datasource, z, x, y):
    result = tile_cache.get(datasource['id'], z, x, y)
    if result:
        return bytes(result[0]), result[1]
    source = datasource['source']
    parts = urlsplit(source)
    base_url = '{0}://{1}'.format(parts.scheme, parts.netloc)
    endpoint = parts.path
    endpoint = endpoint.replace('{z}', str(z))
    endpoint = endpoint.replace('{x}', str(x))
    endpoint = endpoint.replace('{y}', str(y))
    client = getClient(base_url)
    resp = client.get(endpoint)
    tile = resp.content
    mime_type = getMimeTypeFromPath(source)
    tile_cache.set(datasource['id'], mime_type, z, x, y, tile)
    return tile, mime_type

