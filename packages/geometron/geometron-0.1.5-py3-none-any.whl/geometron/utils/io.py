import geopandas as gpd
import pandas as pd
from shapely import wkt

def gdf_from_csv(f, epsg=None):
    epsg = f'epsg:{epsg}' if epsg is not None else epsg
    df = pd.read_csv(f)
    df['geometry'] = df['geometry'].apply(wkt.loads)
    return gpd.GeoDataFrame(df, crs=epsg)