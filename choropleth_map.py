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
pop = 'No'


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
    return data_frame_copy


def json_sources():
    canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
    canada_shape = gpd.read_file(canada)
    canada_shape = canada_shape[['PREABBR', 'geometry']]
    canada_shape = canada_shape.sort_values(by=['PREABBR']).reset_index(
        drop=True)
    canada_shape['geometry'] = canada_shape['geometry'].to_crs(epsg=4326)
    return canada_shape


def df_province_adjust(data_frame):
    df = adjusted_province(data_frame)
    df = df.reset_index(drop=True)
    return df


def data_population_prep(data_frame):
    pop_year = canada_pop.copy()
    merged_data = pop_year.merge(data_frame, left_on='PROVINCE_ADJUSTED',
                                 right_on='PROVINCE_ADJUSTED', how='right')
    merged_data['Quantity_converted'] = merged_data['Quantity_converted'] / \
                                            merged_data['population']
    return merged_data


def data_quantity_adjusted(data_frame):
    df = data_frame
    df['Reporting_Year'] = df['Reporting_Year'] * 1e4 + 101
    df['Reporting_Year'] = pd.to_datetime(
        df['Reporting_Year'].astype('int64').astype('str'))
    datetime_index = pd.DatetimeIndex(df['Reporting_Year'])
    dt_index_epochs = datetime_index.astype(int)
    df['dt_index'] = dt_index_epochs.astype('U10')
    return df


def viz_dict_prep(visualization_frame, shape_frame):
    viz_dict = {}
    for i in shape_frame.index:
        province = shape_frame['PREABBR'][i]
        result = visualization_frame[visualization_frame['PREABBR'] == province]
        inner_dict = {}
        for index, r in result.iterrows():
            inner_dict[r['dt_index']] = {'color': r['color'], 'opacity': 0.7}
        viz_dict[i] = inner_dict
    return viz_dict


def color_scale_prep(visualization_frame):
    max_color = max(visualization_frame['Quantity_converted'])
    min_color = min(visualization_frame['Quantity_converted'])
    cmap = cm.linear.YlOrRd_09.scale(min_color, max_color)
    cmap.caption = "Amount of waste disposed by provinces"
    visualization_frame['color'] = visualization_frame['Quantity_converted']\
        .map(cmap)
    return visualization_frame, cmap


def data_frame_prep(data_frame):
    canada_shape = json_sources()
    viz_frame = pd.merge(data_frame, canada_shape, on="PREABBR")
    viz_frame, cmap = color_scale_prep(viz_frame)
    viz_dict = viz_dict_prep(viz_frame, canada_shape)
    return viz_dict, cmap


def data_for_viz(type_of_method, pop_choice):
    if pop_choice == 'No':
        if type_of_method == 'recycled':
            data_frame = recycle_loc.copy()
            data_frame = df_province_adjust(data_frame)
            data_frame = data_quantity_adjusted(data_frame)
            viz_dict, cmap = data_frame_prep(data_frame)
            return viz_dict, cmap
        elif type_of_method == 'disposed':
            data_frame = dispo_loc.copy()
            data_frame = df_province_adjust(data_frame)
            data_frame = data_quantity_adjusted(data_frame)
            viz_dict, cmap = data_frame_prep(data_frame)
            return viz_dict, cmap
        elif type_of_method == 'total':
            data_frame = merged_recycle_dispo_loc.copy()
            data_frame = df_province_adjust(data_frame)
            data_frame = data_quantity_adjusted(data_frame)
            viz_dict, cmap = data_frame_prep(data_frame)
            return viz_dict, cmap
    elif pop_choice == 'Yes':
        if type_of_method == 'recycled':
            data_frame = recycle_loc.copy()
            data_frame = df_province_adjust(data_frame)
            data_frame = data_population_prep(data_frame)
            data_frame = data_quantity_adjusted(data_frame)
            viz_dict, cmap = data_frame_prep(data_frame)
            return viz_dict, cmap
        elif type_of_method == 'disposed':
            data_frame = dispo_loc.copy()
            data_frame = df_province_adjust(data_frame)
            data_frame = data_population_prep(data_frame)
            data_frame = data_quantity_adjusted(data_frame)
            viz_dict, cmap = data_frame_prep(data_frame)
            return viz_dict, cmap
        elif type_of_method == 'total':
            data_frame = merged_recycle_dispo_loc.copy()
            data_frame = df_province_adjust(data_frame)
            data_frame = data_population_prep(data_frame)
            data_frame = data_quantity_adjusted(data_frame)
            viz_dict, cmap = data_frame_prep(data_frame)
            return viz_dict, cmap
    else:
        raise ValueError('Input validation required')


def choropleth_map(type_of_method, pop_choice):
    canada_shape = json_sources()
    viz_dict, cmap = data_for_viz(type_of_method, pop_choice=pop_choice)
    m = folium.Map(location=[48, -102], zoom_start=4)
    TimeSliderChoropleth(data=canada_shape.to_json(), styledict=viz_dict,
                         name='Waste by province').add_to(m)
    folium.LayerControl().add_to(m)
    m.add_child(cmap)
    m.save('{} and {} to population ratio.html'.format(type_of_method, pop_choice))
    return m


if __name__ == '__main__':
    choropleth_map(type_of_method=method_chosen, pop_choice=pop)
