from typing import List
from typing import Optional

from pydantic import BaseModel


'''
Documentation:
	
	https://nominatim.org/release-docs/develop/api/Search/

'''

class BaseParams(BaseModel):
	addressdetails: Optional[int] = 1
	extratags: Optional[int] = 0
	namedetails: Optional[int] = 0


class ReverseParams(BaseParams):
	lat: float
	lon: float
	zoom: Optional[int] = 18


class SearchParams(BaseParams):
	q: Optional[str] = None
	amenity: Optional[str] = None
	street: Optional[str] = None
	city: Optional[str] = None
	county: Optional[str] = None
	state: Optional[str] = None
	country: Optional[str] = None
	postalcode: Optional[str] = None
	limit: Optional[int] = 10