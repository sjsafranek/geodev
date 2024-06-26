from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

import services.datasources as datasources
import services.geocoder as geocoder
import services.routing as routing
import services.weather as weather

from models.response import ApiStatus
from models.response import ApiResponse


app = FastAPI(title="GeoDev")

app.add_middleware(GZipMiddleware, minimum_size=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

datasources.attach(app, prefix='/api/v1/datasources')
geocoder.attach(app, prefix='/api/v1/geocoder')
routing.attach(app, prefix='/api/v1/routing')
weather.attach(app, prefix='/api/v1/weather')


async def internal_server_exception_handler(request: Request, exc: Exception):
    response = ApiResponse(status=ApiStatus.error, message=str(exc))
    return JSONResponse(
        status_code = 500,
        content = response.dict(exclude_none=True)
    )

app.add_exception_handler(Exception, internal_server_exception_handler)

