import pandas as pd
import folium
import branca.colormap as cm
from folium.plugins import TimeSliderChoropleth
import geopandas as gpd
from explore_visual import merged_recycle_dispo_loc, recycle_loc, dispo_loc
from data_import import canada_pop
import json


year_chosen = 2006
method_chosen = 'recycled'


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


def json_sources(data_frame):
    canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
    canada_shape = gpd.read_file(canada)
    merged_data = canada_shape.merge(data_frame, left_on='PREABBR',
                                     right_on='PROVINCE_ADJUSTED', how='right')
    merged_data.fillna('No data', inplace=True)
    merged_data = merged_data[['PROVINCE_ADJUSTED', 'Quantity_converted']]
    merged_json = json.loads(merged_data.to_json())
    json_data = json.dumps(merged_json)
    return json_data


def data_for_viz(year, type_of_method):
    if type_of_method == 'recycled':
        data_frame = recycle_loc[recycle_loc['Reporting_Year'] == year]
        data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
        data_frame = adjusted_province(data_frame)
        return data_frame
    elif type_of_method == 'disposed':
        data_frame = dispo_loc[dispo_loc['Reporting_Year'] == year]
        data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
        data_frame = adjusted_province(data_frame)
        return data_frame
    elif type_of_method == 'total':
        data_frame = merged_recycle_dispo_loc[merged_recycle_dispo_loc
                                              ['Reporting_Year'] == year]
        data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
        data_frame = adjusted_province(data_frame)
        return data_frame
    else:
        raise ValueError('Input validation required')


def data_merged_pop(year, data_frame):
    pop_year = canada_pop[canada_pop['Reference period'] == year]
    merged_data = pop_year.merge(data_frame, left_on='PROVINCE_ADJUSTED',
                                 right_on='PROVINCE_ADJUSTED', how='right')
    merged_data['Waste_per_pop'] = merged_data['Quantity_converted'] \
                                   / merged_data['population']
    merged_json = json.loads(merged_data.to_json())
    json_data = json.dumps(merged_json)
    return json_data


# Shapefile to json handling
canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
canada_shape = gpd.read_file(canada)
canada_shape = canada_shape[['PREABBR', 'geometry']]
canada_shape = canada_shape.sort_values(by=['PREABBR']).reset_index(drop=True)
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
                                              .astype('int64').astype('str'))
datetime_index = pd.DatetimeIndex(data_frame['Reporting_Year'])
dt_index_epochs = datetime_index.astype(int)
data_frame['dt_index'] = dt_index_epochs.astype('U10')
viz_frame = pd.merge(data_frame, canada_shape, on="PREABBR")

# Color scale for Choropleth
max_color = max(data_frame['Quantity_converted'])
min_color = min(data_frame['Quantity_converted'])
cmap = cm.linear.YlOrRd_09.scale(min_color, max_color)
cmap.caption = "Amount of waste disposed by provinces"
viz_frame['color'] = viz_frame['Quantity_converted'].map(cmap)

# Styledict for TimesliderChoropleth
province_list = canada_shape['PREABBR'].unique().tolist()
province_idx = range(len(province_list))
viz_dict = {}
for i in canada_shape.index:
    province = canada_shape['PREABBR'][i]
    result = viz_frame[viz_frame['PREABBR'] == province]
    inner_dict = {}
    for index, r in result.iterrows():
        inner_dict[r['dt_index']] = {'color': r['color'], 'opacity': 0.7}
    viz_dict[i] = inner_dict

# Choropleth test
m = folium.Map(location=[48, -102], zoom_start=4)
TimeSliderChoropleth(data=canada_shape.to_json(), styledict=viz_dict,
                     name='Waste by province').add_to(m)
folium.LayerControl().add_to(m)
m.add_child(cmap)
m.save('choropleth_test.html')


if __name__ == '__main__':
    print()
