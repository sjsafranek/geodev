import json
import datetime
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils import crypto
from geocoder import database
from utils.HttpClient import HttpClient

router = APIRouter()


client = HttpClient('https://nominatim.openstreetmap.org')


class Params(BaseModel):
	lat: float
	lon: float
	namedetails: int
	zoom: int


def reverse_geocode(lat: float, lon: float, zoom: int = 22, namedetails: int = 1):
	params = {
		'lat': lat,
		'lon': lon,
		'format': 'json',
		'zoom': zoom,
		'namedetails': namedetails
	}
	salt = 'nominatim-reverse-{0}'.format(json.dumps(params))
	key = '{0}'.format(crypto.md5(salt))
	value = database.get(key)
	if value is not None:
		return value[0]
	result = client.getJSON('/reverse', params=params)
	database.set(key, 'nominatim', 'reverse', json.dumps(result))
	return result


@router.get('/reverse', response_class=JSONResponse)
async def get_reverse_geocode(lat: float, lon: float, zoom: int = 22, namedetails: int = 1):
	return reverse_geocode(lat=lat, lon=lon, zoom=zoom, namedetails=namedetails)


@router.post('/reverse', response_class=JSONResponse)
async def post__reverse_reverse(params: Params):
	return reverse_geocode(lat=params.lat, lon=params.lon, zoom=params.zoom, namedetails=params.namedetails)
