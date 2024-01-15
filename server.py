from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware

import services.datasources as datasources
import services.geocoder as geocoder
import services.routing as routing
from models.response import ApiStatus
from models.response import ApiResponse


app = FastAPI(title="GeoDev")

app.add_middleware(GZipMiddleware, minimum_size=500)

# app.include_router(geocoder.router.new(), prefix='/api/v1/geocoder')

geocoder.attach(app, prefix='/api/v1/geocoder')
datasources.attach(app, prefix='/api/v1/datasources')
routing.attach(app, prefix='/api/v1/routing')


async def internal_server_exception_handler(request: Request, exc: Exception):
    response = ApiResponse(status=ApiStatus.error, message=str(exc))
    return JSONResponse(
        status_code = 500,
        content = response.dict(exclude_none=True)
    )

app.add_exception_handler(Exception, internal_server_exception_handler)

