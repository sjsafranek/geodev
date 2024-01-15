from fastapi import Request
from fastapi.responses import JSONResponse

from models.response import ApiStatus
from models.response import ApiResponse


class RoutingException(Exception):
    def __init__(self, path: list):
        self.path = path


async def routing_exception_handler(request: Request, exc: RoutingException):
    response = ApiResponse(status=ApiStatus.error, message=f"Unable to determine route: {';'.join([str(point.wkt) for point in exc.path])}")
    return JSONResponse(
        status_code = 404,
        content = response.dict(exclude_none=True)
    )