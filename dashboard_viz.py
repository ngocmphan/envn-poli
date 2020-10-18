from urllib.request import urlopen
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.plotting import figure
from bokeh.models import Slider, HoverTool
import bokeh
import bokeh.palettes as bp
import geopandas as gpd
from explore_visual import merged_recycle_dispo_loc, recycle_loc, dispo_loc
import matplotlib.pyplot as plt
from data_import import canada_population
import json

year_chosen = 2006
method_chosen = 'recycled'


def adjusted_province(data_frame):
    data_frame_copy = data_frame.copy()
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'AB', 'PROVINCE_ADJUSTED'] = 'Alta.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'BC', 'PROVINCE_ADJUSTED'] = 'B.C.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'MB', 'PROVINCE_ADJUSTED'] = 'Man.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NB', 'PROVINCE_ADJUSTED'] = 'N.B.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NL', 'PROVINCE_ADJUSTED'] = 'N.L.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NS', 'PROVINCE_ADJUSTED'] = 'N.S.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NT', 'PROVINCE_ADJUSTED'] = 'N.W.T.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'NU', 'PROVINCE_ADJUSTED'] = 'Nvt.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'ON', 'PROVINCE_ADJUSTED'] = 'Ont.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'PE', 'PROVINCE_ADJUSTED'] = 'P.E.I.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'QC', 'PROVINCE_ADJUSTED'] = 'Que.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'SK', 'PROVINCE_ADJUSTED'] = 'Sask.'
    data_frame_copy.loc[data_frame
                        ['PROVINCE'] == 'YT', 'PROVINCE_ADJUSTED'] = 'Y.T.'
    data_frame_copy = data_frame_copy[['PROVINCE_ADJUSTED',
                                       'Quantity_converted']]
    return data_frame_copy


def json_sources(data_frame):
    canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
    canada_shape = gpd.read_file(canada)
    merged_data = canada_shape.merge(data_frame, left_on='PREABBR',
                                     right_on='PROVINCE_ADJUSTED', how='left')
    json_data = json.dumps(json.loads(merged_data.to_json()))
    return GeoJSONDataSource(geojson=json_data)


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


def bokeh_choropleth(gdf, column=None, title=''):
    geosource = json_sources(gdf)
    palette = bp.brewer['OrRd'][8]
    palette = palette[::-1]
    vals = gdf[column]

    color_mapper = LinearColorMapper(palette=palette, low=vals.min(),
                                     high=vals.max())
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500,
                         height=20, location=(0, 0), orientation='horizontal')
    tools = 'wheel_zoom,pan,reset'
    p = figure(title=title, plot_height=400, plot_width=850,
               toolbar_location='right', tools=tools)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.patches('xs', 'ys', source=geosource, fill_alpha=1, line_width=0.5,
              line_color='black',
              fill_color={'field': column, 'transform': color_mapper})
    p.add_layout(color_bar, 'below')
    bokeh.plotting.output_file('{}.html'.format(title))
    bokeh.plotting.save(p)
    bokeh.plotting.show(p)
    return p


data = data_for_viz(year_chosen, method_chosen)
bokeh_choropleth(data, 'Quantity_converted', 'test_choropleth')

if __name__ == '__main__':
    print()
