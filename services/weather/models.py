from pydantic import BaseModel
from typing import Optional


class WeatherParams(BaseModel):
	longitude: float
	latitude: float
	radius: Optional[int] = 50
	precision: Optional[int] = 2