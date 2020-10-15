import plotly.express as px
from urllib.request import urlopen
import geopandas as gpd
from explore_visual import merged_recycle_dispo_loc, recycle_loc, dispo_loc
from data_import import canada_population
import json

year_chosen = 2006
method_chosen = 'recycled'


def adjusted_province(data_frame):
    data_frame_copy = data_frame.copy()
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'AB', 'PROVINCE_ADJUSTED'] = 'Alta.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'BC', 'PROVINCE_ADJUSTED'] = 'B.C'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'MB', 'PROVINCE_ADJUSTED'] = 'Man.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NB', 'PROVINCE_ADJUSTED'] = 'N.B.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NL', 'PROVINCE_ADJUSTED'] = 'N.L.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NS', 'PROVINCE_ADJUSTED'] = 'N.S.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NT', 'PROVINCE_ADJUSTED'] = 'N.W.T'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NU', 'PROVINCE_ADJUSTED'] = 'Nvt.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'ON', 'PROVINCE_ADJUSTED'] = 'Ont.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'PE', 'PROVINCE_ADJUSTED'] = 'P.E.I'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'QC', 'PROVINCE_ADJUSTED'] = 'Que.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'SK', 'PROVINCE_ADJUSTED'] = 'Sask.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'YT', 'PROVINCE_ADJUSTED'] = 'Y.T.'
    return data_frame_copy


def json_sources(data_frame):
    canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
    canada_shape = gpd.read_file(canada)
    merged_data = canada_shape.merge(data_frame, left_on='PREABBR',
                                     right_on='PROVINCE_ADJUSTED')
    merged_json = json.loads(merged_data.to_json())
    json_data = json.dumps(merged_json)
    return json_data


def data_for_viz(year, type_of_method):
    if type_of_method == 'recycled':
        data_frame = recycle_loc[recycle_loc['Reporting_Year'] == year]
        data_frame = adjusted_province(data_frame)
        data_source = json_sources(data_frame)
        return data_source
    elif type_of_method == 'disposed':
        data_frame = dispo_loc[dispo_loc['Reporting_Year'] == year]
        data_frame = adjusted_province(data_frame)
        data_source = json_sources(data_frame)
        return data_source
    elif type_of_method == 'total':
        data_frame = merged_recycle_dispo_loc[merged_recycle_dispo_loc
                                              ['Reporting_Year'] == year]
        data_frame = adjusted_province(data_frame)
        data_source = json_sources(data_frame)
        return data_source
    else:
        raise ValueError('Input validation required')


if __name__ == '__main__':
    print()
