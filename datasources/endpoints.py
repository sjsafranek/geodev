from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse

from datasources import database


router = APIRouter()



# @router.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )




@router.get('/', response_class=JSONResponse)
async def get_datasources():
	return database.fetchall()


@router.get('/{datasource_id}', response_class=JSONResponse)
async def get_datasource(datasource_id: str):
	datasource = database.fetch(datasource_id)
	if not datasource:
		raise HTTPException(status_code=404, detail="Datasource not found")
	return datasource


@router.get('/{datasource_id}/tile/{z}/{x}/{y}', response_class=JSONResponse)
async def get_tile(datasource_id: str, z: int, x: int, y: int):
	datasource = database.fetch(datasource_id)
	print(datasource)
	return None
