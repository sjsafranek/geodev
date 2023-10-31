from fastapi import APIRouter

from geocoder import nominatim


def new():
	router = APIRouter()
	router.include_router(nominatim.router, tags=['osm', 'nominatim'])
	# router.include_router(nominatim.router, prefix='/nominatim', tags=['osm', 'nominatim'])
	return router