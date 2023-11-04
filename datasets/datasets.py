import os.path
import zipfile

import pandas
import geopandas
from shapely.geometry import Point

import conf


def load_cities():
    filename = os.path.join(conf.DATA_DIRECTORY, 'simplemaps_worldcities_basicv1.76.zip')
    with zipfile.ZipFile(filename) as zh:
        df = pandas.read_csv(zh.open('worldcities.csv'))
        df['geometry'] = df.apply(lambda row: Point(row['lng'], row['lat']), axis=1)
        gdf = geopandas.GeoDataFrame(df, crs='EPSG:4326').set_geometry('geometry')
        return gdf 
