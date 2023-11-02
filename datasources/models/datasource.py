
from datetime import datetime

from typing import List
from typing import Optional

from pydantic import BaseModel


class Datasource(BaseModel):
	id: str
	name: str
	type: str
	source: str
	description: Optional[str]
	srid: int	
	is_updatable: bool
	is_deleted: bool
	created_at: datetime
	updated_at: datetime

	@property
	def has_tiles(self):
	    return self.type in ['TiledMapService', 'MapboxVectorTile']

