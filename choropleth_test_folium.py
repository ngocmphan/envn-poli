import pandas as pd
import geopandas as gpd
import json
from explore_visual import recycle_loc
import folium
import webbrowser

# Shapefile to json handling
canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
canada_shape = gpd.read_file(canada)
canada_shape = canada_shape[['PREABBR', 'geometry']]
canada_shape['geometry'] = canada_shape['geometry'].to_crs(epsg=4326)
canada_shape.to_file('canada.json', driver='GeoJSON')
canada_geo = '/Users/ngocphan/PycharmProjects/envn_poli/canada.json'

# Data frame handling


def adjusted_province(data_frame):
    data_frame_copy = data_frame.copy()
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'AB', 'PREABBR'] = 'Alta.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'BC', 'PREABBR'] = 'B.C.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'MB', 'PREABBR'] = 'Man.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NB', 'PREABBR'] = 'N.B.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NL', 'PREABBR'] = 'N.L.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NS', 'PREABBR'] = 'N.S.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NT', 'PREABBR'] = 'N.W.T.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NU', 'PREABBR'] = 'Nvt.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'ON', 'PREABBR'] = 'Ont.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'PE', 'PREABBR'] = 'P.E.I.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'QC', 'PREABBR'] = 'Que.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'SK', 'PREABBR'] = 'Sask.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'YT', 'PREABBR'] = 'Y.T.'
    data_frame_copy = data_frame_copy[['PREABBR',
                                       'Quantity_converted']]
    return data_frame_copy


data_frame = recycle_loc[recycle_loc['Reporting_Year'] == 2006]
data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
data_frame = adjusted_province(data_frame)
data_frame = data_frame.reset_index(drop=True)


# Choropleth test
m = folium.Map(location=[48, -102], zoom_start=4)
bins = list(data_frame['Quantity_converted'].quantile([0, 0.25, 0.5, 0.75, 1]))
folium.Choropleth(
    geo_data=canada_geo,
    name='choropleth',
    data=data_frame,
    columns=['PREABBR', 'Quantity_converted'],
    key_on='feature.properties.PREABBR',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Waste Produced in 000',
    bins=bins,
    reset=True
).add_to(m)
folium.LayerControl().add_to(m)

m.save('choropleth_test.html')
url = 'choropleth_test.html'


if __name__ == '__main__':
    print()
