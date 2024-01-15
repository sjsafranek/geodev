
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from services.datasources import database
from services.datasources import exceptions
import services.datasources.models as models
from models.response import ApiStatus
from models.response import ApiResponse


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
    if not datasource:
        raise exceptions.DatasourceNotFoundException(datasource_id);

    datasource = models.from_dict(datasource)
    if not datasource.has_tiles:
        raise Exception(f"{datasource.type} not supported")

    tile, media_type = datasource.fetchTile(z, x, y)
    return Response(content=tile, media_type=media_type)

