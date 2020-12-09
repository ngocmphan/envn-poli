import pandas as pd
import geopandas as gpd
import json
from explore_visual import recycle_loc
import folium
import webbrowser
import branca.colormap as cm
from folium.plugins import TimeSliderChoropleth
import datetime as dt

# Shapefile to json handling
canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
canada_shape = gpd.read_file(canada)
canada_shape = canada_shape[['PREABBR', 'geometry']]
canada_shape = canada_shape.sort_values(by=['PREABBR']).reset_index(drop=True)
print(canada_shape)
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
    data_frame_copy = data_frame_copy[['Reporting_Year', 'PREABBR',
                                       'Quantity_converted']]
    return data_frame_copy


data_frame = recycle_loc.copy()
data_frame = adjusted_province(data_frame)
data_frame = data_frame.reset_index(drop=True)

# Datetime handling
data_frame['Reporting_Year'] = data_frame['Reporting_Year']*1e4+101
data_frame['Reporting_Year'] = pd.to_datetime(data_frame['Reporting_Year']
                                              .astype('int64').
                                              astype(str), yearfirst=True)

datetime_index = pd.DatetimeIndex(data_frame['Reporting_Year'])
dt_index_epochs = datetime_index.astype(int)
dt_index = dt_index_epochs.astype('U10')
viz_frame = pd.merge(data_frame, canada_shape, on="PREABBR")

# Color scale for Choropleth
max_color = max(data_frame['Quantity_converted'])
min_color = min(data_frame['Quantity_converted'])
cmap = cm.linear.YlOrRd_09.scale(min_color, max_color)
data_frame['color'] = data_frame['Quantity_converted'].map(cmap)

# Styledict for TimesliderChoropleth
province_list = data_frame['PREABBR'].unique().tolist()
province_idx = range(len(province_list))
viz_dict = {}
for i in province_idx:
    province = province_list[i]
    result = data_frame[data_frame['PREABBR'] == province]
    inner_dict = {}
    for index, r in result.iterrows():
        inner_dict[r['Reporting_Year']] = {'color': r['color'], 'opacity': 0.7}
    viz_dict[i] = inner_dict

# Choropleth test
m = folium.Map(location=[48, -102], zoom_start=4)
# folium.Choropleth(
#     geo_data=canada_geo,
#     name='choropleth',
#     data=data_frame,
#     columns=['PREABBR', 'Quantity_converted'],
#     key_on='feature.properties.PREABBR',
#     fill_color='BuPu',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Waste Produced in 000',
#     bins=bins,
#     reset=True
# ).add_to(m)

# TimeSliderChoropleth(data=data_frame.to_json(), styledict=viz_dict,
#                      name='Waste by province').add_to(m)
# folium.LayerControl().add_to(m)
#
# m.save('choropleth_test.html')


if __name__ == '__main__':
    print()
