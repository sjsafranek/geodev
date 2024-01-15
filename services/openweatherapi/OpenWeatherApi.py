import json
import time
import datetime
import pandas
import geopandas
from shapely import wkt
from shapely.geometry import Point

import conf
import crypto
from openweatherapi import database
from utils.HttpClient import HttpClient


OPENWEATHERAPI_APIKEY = conf.get_credential("openweatherapi")['apikey']
MAX_AGE = datetime.timedelta(seconds=3600)
BASE_URL = "https://api.openweathermap.org"

client = HttpClient(BASE_URL)


def _get(key):
    data = database.get(key)
    if data:  
        df = pandas.DataFrame.from_dict(data[0])
        df['geometry'] = df['geometry'].apply(wkt.loads)
        gdf = geopandas.GeoDataFrame(df, crs='EPSG:4326').set_geometry('geometry')
        return gdf
    return None


def _set(key, gdf):
    data = gdf.to_dict()
    geometry = {}
    for _id in data['geometry']:
        geometry[_id] = data['geometry'][_id].wkt
    data['geometry'] = geometry
    database.set(key, json.dumps(data), max_age=MAX_AGE)


def _buildGeoDataFrame(response):
    data = {
        'id': [],
        'name': [],
        'geometry': [],
        'temp': [],
        'rain': [],
        'snow': [],
        'clouds': [],
        "pressure": [] ,
        "humidity": [],
        'weather': [],
        'description': []
    }
    if 'list' in response:
        places = response['list']
        for place in places:
            # print(place)
            point = Point(place['coord']['lon'], place['coord']['lat'])
            data['id'].append(place['id'])
            data['name'].append(place['name'])
            data['geometry'].append(point)
            data['temp'].append(place['main']['temp'])
            data['rain'].append(None)
            data['snow'].append(None)
            data['clouds'].append(place['clouds']['all'])
            data['pressure'].append(place['main']['pressure'])
            data['humidity'].append(place['main']['humidity'])
            data['weather'].append(place['weather'][0]['main'])
            data['description'].append(place['weather'][0]['description'])
    gdf = geopandas.GeoDataFrame(data, crs='EPSG:4326')
    gdf.set_index('id', inplace=True)
    gdf['created_at'] = int(time.time())
    gdf['expires_at'] = gdf['created_at'] + 3600
    return gdf

def _getJSON(endpoint, params={}):
    requestId = crypto.md5(endpoint+json.dumps(params))
    key = "weather-{0}".format(requestId)
    gdf = _get(key)
    if gdf is not None:
        return gdf
    params['appid'] = OPENWEATHERAPI_APIKEY
    response = client.getJSON(endpoint, params=params, headers={'Accept-Language': 'en-US,en;q=0.5'})
    gdf = _buildGeoDataFrame(response)
    gdf['request_id'] = requestId
    _set(key, gdf)
    return gdf


def _getWeatherAroundPoint(point, params={}):
    return _getJSON('/data/2.5/find', params=params)


def getWeatherAroundPoint(point, radius=50, precision=2):
    return _getWeatherAroundPoint('/data/2.5/find', params={
        'lat': round(point.y, precision),
        'lon': round(point.x, precision),
        'cnt': radius
    })


# def getWeatherByPoint(point):
#     return client.getJSON('/data/2.5/weather', params={
#         'lat': point.y,
#         'lon': point.x
#     })


# def getWeatherByPlaceName(place_name):
#     return client.getJSON('/data/2.5/weather', params={
#         'q': place_name
#     })