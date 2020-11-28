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
canada_shape = canada_shape.set_index('PREABBR')
canada_shape.to_file('canada.geojson', driver='GeoJSON', index='PREABBR')

canada_geo = '/Users/ngocphan/PycharmProjects/envn_poli/canada.geojson'

# Data frame handling


def adjusted_province(data_frame):
    data_frame_copy = data_frame.copy()
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'AB', 'PROVINCE_ADJUSTED'] = 'Alta.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'BC', 'PROVINCE_ADJUSTED'] = 'B.C.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'MB', 'PROVINCE_ADJUSTED'] = 'Man.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NB', 'PROVINCE_ADJUSTED'] = 'N.B.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NL', 'PROVINCE_ADJUSTED'] = 'N.L.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NS', 'PROVINCE_ADJUSTED'] = 'N.S.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NT', 'PROVINCE_ADJUSTED'] = 'N.W.T.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'NU', 'PROVINCE_ADJUSTED'] = 'Nvt.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'ON', 'PROVINCE_ADJUSTED'] = 'Ont.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'PE', 'PROVINCE_ADJUSTED'] = 'P.E.I.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'QC', 'PROVINCE_ADJUSTED'] = 'Que.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'SK', 'PROVINCE_ADJUSTED'] = 'Sask.'
    data_frame_copy.loc[data_frame_copy
                        ['PROVINCE'] == 'YT', 'PROVINCE_ADJUSTED'] = 'Y.T.'
    data_frame_copy = data_frame_copy[['PROVINCE_ADJUSTED',
                                       'Quantity_converted']]
    return data_frame_copy


data_frame = recycle_loc[recycle_loc['Reporting_Year'] == 2006]
data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
data_frame = adjusted_province(data_frame)


# Choropleth test
m = folium.Map(location=[48, -102], zoom_start=4)
bins = list(data_frame['Quantity_converted'].quantile([0, 0.25, 0.5, 0.75, 1]))
folium.Choropleth(
    geo_data=canada_geo,
    name='choropleth',
    data=data_frame,
    columns=['PROVINCE_ADJUSTED', 'Quantity_converted'],
    key_on='feature.properties.PREABBR',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Waste Produced in 000',
    bins=bins,
    reset=True
).add_to(m)
folium.LayerControl().add_to(m)

m.save('choropleth_test.html')
url = 'choropleth_test.html'
webbrowser.open(url)


if __name__ == '__main__':
    print()
