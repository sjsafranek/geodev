import json
import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils import crypto
from geocoder import models
from geocoder import database
from utils.HttpClient import HttpClient


router = APIRouter()


client = HttpClient('https://nominatim.openstreetmap.org')


def send(endpoint, params={}):
	salt = 'nominatim-{0}-{1}'.format(endpoint, json.dumps(params))
	key = '{0}'.format(crypto.md5(salt))
	value = database.get(key)
	if value is not None:
		return value[0]
	result = client.getJSON(endpoint, params=params)
	database.set(key, 'nominatim', endpoint, json.dumps(result))
	return result


def reverse(params: models.ReverseParams):
	params = {
		'format': 'json',	
		'lat': params.lat,
		'lon': params.lon,
		'zoom': params.zoom,
		'namedetails': params.namedetails
	}
	return send('/reverse', params=params)
	# salt = 'nominatim-reverse-{0}'.format(json.dumps(params))
	# key = '{0}'.format(crypto.md5(salt))
	# value = database.get(key)
	# if value is not None:
	# 	return value[0]
	# result = client.getJSON('/reverse', params=params)
	# database.set(key, 'nominatim', 'reverse', json.dumps(result))
	# return result


def geocode(params: models.SearchParams):
	params = {
		'format': 'json',
		'q': params.q, 
		'amenity': params.amenity, 
		'street': params.street, 
		'city': params.city, 
		'county': params.county, 
		'state': params.state, 
		'country': params.country, 
		'postalcode': params.postalcode
	}
	return send('/search', params=params)
	# salt = 'nominatim-search-{0}'.format(json.dumps(params))
	# key = '{0}'.format(crypto.md5(salt))
	# value = database.get(key)
	# if value is not None:
	# 	return value[0]
	# result = client.getJSON('/search', params=params)
	# database.set(key, 'nominatim', 'search', json.dumps(result))
	# return result


@router.post('/reverse', response_class=JSONResponse)
async def post_reverse_geocode(params: models.ReverseParams):
	return reverse(params)


@router.post('/search', response_class=JSONResponse)
async def post_geocode(params: models.SearchParams):
	return geocode(params)

