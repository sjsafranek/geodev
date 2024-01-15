import json
from shapely.geometry import Point

from services.routing.exceptions import *
from utils.HttpClient import HttpClient


BASE_URL = 'https://router.project-osrm.org'
client = HttpClient(BASE_URL)


def _fetch(path):
    endpoint = '/route/v1/driving/{0}'.format(';'.join([f'{point.x},{point.y}' for point in path]))
    return client.getJSON(endpoint, params={
                    'overview': 'false',
                    'alternatives': 'true',
                    'steps': 'true',
                    'geometries': 'geojson'
                })

def route(path):
    response = _fetch(path)
    if 'ok' != response['code'].lower():
        raise RoutingException(path)
    if 0 == len(response['routes']):
        raise RoutingException(path)
    coordinates = []
    for leg in response['routes'][0]['legs']:
        for step in leg['steps']:
            coordinates += step['geometry']['coordinates']
    return {'type': 'LineString', 'coordinates': coordinates}

