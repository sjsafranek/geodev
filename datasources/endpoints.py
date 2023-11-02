
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from datasources import database
from datasources import exceptions
from datasources.models.datasource import Datasource
from datasources.models.tile_layer import TileLayer
from models.response import ApiStatus
from models.response import ApiResponse
# from datasources import tile_proxy


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


@router.get('/{datasource_id}/tile/{z}/{x}/{y}.{ext}', response_class=JSONResponse)
async def get_tile(datasource_id: str, z: int, x: int, y: int, ext: str):
    datasource = database.fetch(datasource_id)

    # print(dir(Datasource))
    # print(datasource)

    if datasource['type'] not in ['TiledMapService', 'MapboxVectorTile']:
        raise Exception(f"{datasource['type']} not supported")

    layer = TileLayer(**datasource)
    tile, media_type = layer.fetchTile(z, x, y)
    return Response(content=tile, media_type=media_type)

