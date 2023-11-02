from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel


class ApiStatus(str, Enum):
    ok = "ok"
    error = "error"


class ApiResponse(BaseModel):
	status: ApiStatus = ApiStatus.ok
	data: Optional[dict] = None
	message: Optional[str] = None
