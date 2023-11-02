
from datasources import tile_proxy
from datasources.models.datasource import Datasource


class TileLayer(Datasource):
	
	def fetchTile(self, z, x, y):
		return tile_proxy.fetch(self.dict(), z, x, y)

