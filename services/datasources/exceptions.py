from fastapi import Request
from fastapi.responses import JSONResponse

from models.response import ApiStatus
from models.response import ApiResponse


class DatasourceNotFoundException(Exception):
    def __init__(self, datasource_id: str):
        self.datasourceId = datasource_id


async def datasource_not_found_handler(request: Request, exc: DatasourceNotFoundException):
    response = ApiResponse(status=ApiStatus.error, message=f"Datasource '{exc.datasourceId}' not found")
    return JSONResponse(
        status_code = 404,
        content = response.dict(exclude_none=True)
    )