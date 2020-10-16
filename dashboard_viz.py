from urllib.request import urlopen
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.plotting import figure
from bokeh.models import Slider, HoverTool
import bokeh
import bokeh.palettes as bp
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
    data_frame_copy = data_frame_copy[['PROVINCE_ADJUSTED',
                                       'Quantity_converted']]
    return data_frame_copy


def json_sources(data_frame):
    canada = r'lpr_000b16a_e/lpr_000b16a_e.shp'
    canada_shape = gpd.read_file(canada)
    merged_data = canada_shape.merge(data_frame, left_on='PREABBR',
                                     right_on='PROVINCE_ADJUSTED')
    merged_json = json.loads(merged_data.to_json())
    json_data = json.dumps(merged_json)
    geosource = GeoJSONDataSource(geojson=json_data)
    return geosource


def data_for_viz(year, type_of_method):
    if type_of_method == 'recycled':
        data_frame = recycle_loc[recycle_loc['Reporting_Year'] == year]
        data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
        data_frame = adjusted_province(data_frame)
        data_source = json_sources(data_frame)
        return data_source
    elif type_of_method == 'disposed':
        data_frame = dispo_loc[dispo_loc['Reporting_Year'] == year]
        data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
        data_frame = adjusted_province(data_frame)
        data_source = json_sources(data_frame)
        return data_source
    elif type_of_method == 'total':
        data_frame = merged_recycle_dispo_loc[merged_recycle_dispo_loc
                                              ['Reporting_Year'] == year]
        data_frame = data_frame[['PROVINCE', 'Quantity_converted']]
        data_frame = adjusted_province(data_frame)
        data_source = json_sources(data_frame)
        return data_source
    else:
        raise ValueError('Input validation required')


data_viz = data_for_viz(year_chosen, method_chosen)
palette = bp.brewer['YlGnBu'][8]
palette = palette[::-1]
color_mapper = LinearColorMapper(palette=palette, low=0, high=100000,
                                 nan_color='#d9d9d9')
hover = HoverTool(tooltips=[('Country/region', '@PROVINCE_ADJUSTED'),
                             ('Amount of Waste', '@Quantity_converted')])
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal')

p = figure(title='Wast released by provinces, 2006',
           plot_height=600, plot_width=950, toolbar_location=None, tools=[hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

# Add patch renderer to figure.
p.patches('xs', 'ys', source=data_viz,
          fill_color={'field': 'Quantity_converted', 'transform': color_mapper},
          line_color='black', line_width=0.25, fill_alpha=1)
p.add_layout(color_bar)

bokeh.plotting.output_file('test_heatmap.html')

print(recycle_loc[recycle_loc['PROVINCE'] == 'QC'])

if __name__ == '__main__':
    print()
