import json
import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils import crypto
from geocoder import database
from utils.HttpClient import HttpClient

router = APIRouter()


client = HttpClient('https://nominatim.openstreetmap.org')


@router.get('/reverse', response_class=JSONResponse)
@router.post('/reverse', response_class=JSONResponse)
async def reverse(lat: float, lon: float, zoom: int = 22, namedetails: int = 1):
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
