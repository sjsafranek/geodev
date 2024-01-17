
from services.weather import endpoints


def attach(app, prefix=None):
	app.include_router(endpoints.router, prefix=prefix, tags=['weather', 'openweatherapi'])