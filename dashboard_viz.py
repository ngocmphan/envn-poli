import plotly.express as px
from urllib.request import urlopen
import geopandas as gpd

canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
canada_shape = gpd.read_file(canada)

if __name__ == '__main__':
    print()
