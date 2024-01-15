from typing import List
from pydantic import BaseModel
from pydantic import conlist


class Point(BaseModel):
	longitude: float
	latitude: float


class RouteParams(BaseModel):
	path: conlist(List[float], min_length=2, max_length=2)