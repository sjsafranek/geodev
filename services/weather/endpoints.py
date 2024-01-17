import json
import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from shapely.geometry import Point

from utils import crypto
from services.weather import OpenWeatherApi
from services.weather import models
from utils.HttpClient import HttpClient


router = APIRouter()


@router.post('/find', response_class=JSONResponse)
async def post_find(params: models.WeatherParams):
	gdf = OpenWeatherApi.getWeatherAroundPoint(Point(params.longitude, params.latitude), radius=params.radius, precision=params.precision)
	return json.loads(gdf.to_json())

