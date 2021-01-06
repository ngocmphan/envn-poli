import dash
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    html.H1('Waste management in Canada analysis 2006-2016'),
    html.H2('Amount of waste produced by Canadian provinces'),
    html.Iframe(id='map', srcDoc=open('recycled and No to '
                                      'population ratio.html', 'r').read(),
                width='50%', height='600'),
    html.H2('Ratio of waste over provincial population '
            'of Canadian provinces'),
    html.Iframe(id='map', srcDoc=open('recycled and Yes to '
                                      'population ratio.html', 'r').read(),
                width='50%', height='600')

])


if __name__ == '__main__':
    app.run_server(debug=True)
