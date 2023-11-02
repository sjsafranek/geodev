from urllib.parse import urlsplit

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from datasources import database
from datasources import exceptions
from models.response import ApiStatus
from models.response import ApiResponse
from utils.HttpClient import HttpClient


router = APIRouter()


@router.get('/', response_class=JSONResponse)
async def get_datasources():
    response = ApiResponse(data = {"datasources": database.fetchall()})
    return JSONResponse(
        content = response.dict(exclude_none=True)
    )


@router.get('/{datasource_id}', response_class=JSONResponse)
async def get_datasource(datasource_id: str):
    datasource = database.fetch(datasource_id)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(datasource_id);
    response = ApiResponse(data = {"datasource": datasource})
    return JSONResponse(
        content = response.dict(exclude_none=True)
    )



clients = {}

@router.get('/{datasource_id}/tile/{z}/{x}/{y}.{ext}', response_class=JSONResponse)
async def get_tile(datasource_id: str, z: int, x: int, y: int, ext: str):
    datasource = database.fetch(datasource_id)
    if datasource['type'] not in ['TiledMapService', 'MapboxVectorTile']:
        raise Exception(f"{datasource['type']} not supported")

    parts = urlsplit(datasource['source'])
    base_url = '{0}://{1}'.format(parts.scheme, parts.netloc)
    if base_url not in clients:
        clients[base_url] = HttpClient(base_url)

    endpoint = parts.path
    endpoint = endpoint.replace('{z}', str(z))
    endpoint = endpoint.replace('{x}', str(x))
    endpoint = endpoint.replace('{y}', str(y))
    resp = clients[base_url].get(endpoint, headers={'User-Agent': 'geodev/0.0.1'})
    return Response(content=resp.content, media_type="image/png")

