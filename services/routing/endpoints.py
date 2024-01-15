import json
import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from shapely.geometry import Point

from utils import crypto
from services.routing import osrm
from services.routing import models
from utils.HttpClient import HttpClient


router = APIRouter()


def send(path):
	# salt = 'osrm-{0}'.format(json.dumps(path))
	# key = '{0}'.format(crypto.md5(salt))
	# value = route_cache.get(key)
	# if value is not None:
	# 	return value[0]
	geometry = osrm.route(path)
	#route_cache.set(key, 'osrm', endpoint[1:], json.dumps(geometry))
	return geometry



@router.post('/route', response_class=JSONResponse)
async def post_route(params: models.RouteParams):
	return route([Point(location[0], location[1]) for location in params.path])







# longitude = -123.022049
# latitude = 44.046188
# springfield = Point(longitude, latitude)

# longitude = -122.676483
# latitude = 45.523064
# portland = Point(longitude, latitude)

# geometry = osrm.route([springfield, portland])
# print(json.dumps(geometry))