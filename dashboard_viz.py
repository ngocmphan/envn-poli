from urllib.request import urlopen
from bokeh.models import GeoJSONDataSource, LinearColorMapper, Slider, HoverTool
from bokeh.plotting import figure
from bokeh.models.glyphs import Patches
from bokeh.layouts import widgetbox, row, column
import bokeh
import bokeh.palettes as bp
import geopandas as gpd
from explore_visual import merged_recycle_dispo_loc, recycle_loc, dispo_loc
from data_import import canada_pop
from bokeh.io import curdoc
import json
from datetime import datetime

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


# def update_plot(attr, old, new):
#     yr = slider.value
#     new_data = data_for_viz(yr, type_of_method)
#     vals = new_data[column]
#     color_mapper.low = vals.min()
#     color_mapper.high = vals.max()
#     geosource.geojson = new_data.to_json()
#     p.add_tools(HoverTool(tooltips=[('PROVINCE', '@PROVINCE_ADJUSTED'),
#                 ('Amount of waste', '@Quantity_converted{int}')]))


def bokeh_choropleth(year, type_of_method, title=''):
    column = 'Quantity_converted'
    gdf = data_for_viz(year, type_of_method)
    geosource = GeoJSONDataSource(geojson=json_sources(gdf))

    palette = bp.brewer['OrRd'][9]
    palette = palette[::-1]
    vals = gdf[column]

    color_mapper = LinearColorMapper(palette=palette, low=vals.min(),
                                     high=vals.max(), nan_color='#d9d9d9')
    # tools = 'wheel_zoom,pan,reset'
    TOOLTIP = [('PROVINCE', '@PROVINCE_ADJUSTED'),
               ('Amount of waste', '@Quantity_converted{int}')]
    hover = HoverTool(tooltips=TOOLTIP)
    color_bar = bokeh.models.ColorBar(color_mapper=color_mapper, label_standoff=8, width=500,
                                         height=20,
                                         border_line_color=None, location=(0, 0),
                                         orientation='horizontal')

    p = figure(title=title, plot_width=750, plot_height=500,
               toolbar_location='right', tools=[hover])
    p.patches('xs', 'ys', source=geosource, fill_alpha=1, line_width=0.3,
              line_color='black',
              fill_color={'field': column, 'transform': color_mapper})

    p.add_layout(color_bar, 'below')

    def update_plot(attr, old, new):
        yr = slider.value
        new_data = data_for_viz(yr, type_of_method)
        vals = new_data[column]
        color_mapper.low = vals.min()
        color_mapper.high = vals.max()
        geosource.geojson = new_data.to_json()
        p.add_tools(HoverTool(tooltips=[('PROVINCE', '@PROVINCE_ADJUSTED'),
                                        ('Amount of waste',
                                         '@Quantity_converted{int}')]))

    slider = Slider(title='Year', start=2006, end=2016, step=1, value=2006)
    slider.on_change('value', update_plot)
    layout = bokeh.layouts.layout(p, bokeh.models.Column(slider))
    curdoc().add_root(layout)
    bokeh.plotting.output_file('{}.html'.format(title))
    return layout


def dashboard_viz(dashboard_1, dashboard_2):
    return True


bokeh_choropleth(year_chosen, method_chosen, 'Test_choropleth_Nov13')
if __name__ == '__main__':
    print()
