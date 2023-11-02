from fastapi import APIRouter

from datasources import endpoints
from datasources import exceptions


def attach(app, prefix=None):
	app.include_router(endpoints.router, prefix=prefix)
	app.add_exception_handler(exceptions.DatasourceNotFoundException, exceptions.datasource_not_found_handler)
