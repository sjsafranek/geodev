from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

import geocoder.router

app = FastAPI(title="GeoDev")

app.add_middleware(GZipMiddleware, minimum_size=500)
app.include_router(geocoder.router.new(), prefix='/api/v1/geocoder')
