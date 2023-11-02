from fastapi import APIRouter

from datasources import endpoints


def new():
	router = APIRouter()
	router.include_router(endpoints.router)
	return router