
from services.routing import endpoints


def attach(app, prefix=None):
	app.include_router(endpoints.router, prefix=prefix, tags=['osrm', 'routing'])