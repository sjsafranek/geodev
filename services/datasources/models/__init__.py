
from services.datasources.models.datasource import Datasource
from services.datasources.models.tile_layer import TileLayer


def from_dict(data):
	if data['type'] in ['TiledMapService', 'MapboxVectorTile']:
		return TileLayer(**data) 
	return Datasource(**data)
