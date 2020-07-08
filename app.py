import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# self-defined python modules begin here
from view import fatality_rates_var_chart_tab, incident_jitter_boxplot_tab, \
    incident_horizontal_bar_chart, jitter_bar_fatality_chart
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True
server = app.server
app.title = 'Flight Explorer'
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.Img(src='https://storage.needpix.com/rsynced_images/airplane-26560_1280.png',
                         width='100px'),
                html.H1("Flight Explorer", className="display-3"),
                html.P(
                    "an interactive dashboard for looking at flight incident data",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)
footer = dbc.Container([dbc.Row(dbc.Col([html.P("""Made by James Liu, Lise Braaten, Tao Huang
                                        of DSCI 532 group 111 as a collaborative project"""),
                                        dcc.Markdown("""data taken from [github](https://github.com/fivethirtyeight/data/tree/master/airline-safety), 
                                        originally used for 
                                        [this fiveThirtyEight article.](https://fivethirtyeight.com/features/should-travelers-avoid-flying-airlines-that-have-had-crashes-in-the-past/)""")])),
                        ])
app.layout = html.Div([
    jumbotron,
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Fatality rates per billion by airlines', value='tab-1'),
        dcc.Tab(label='Counts of different categories of incidents', value='tab-2'),
    ]),
    html.Div(id='tabs-content'),
    footer
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    """
    retrieves the tab page depending on click.

    Parameters
    ----------
    tab: the tab value indicating tab 1 or 2

    Returns
    -------
    dcc.Tab object containing the specified tab.

    """
    if tab == 'tab-1':
        return fatality_rates_var_chart_tab.return_fatality_rates_bar_chart_result()
    elif tab == 'tab-2':
        return incident_jitter_boxplot_tab.return_incident_jitter_boxplot_result()


@app.callback(Output('horizontal_bar_chart_iframe', 'srcDoc'),
              [Input('radio-items', 'value')])
def render_incident_horizontal_bar_chart(value):
    """
    renders the incident bar chart depending on the selection of the radio buttons.

    Parameters
    ----------
    value: one of "0", "1" or "2",
        which stands for first-world countries, non-first-world countries, or both, respectively.

    Returns
    -------
        an html object representing the alt.chart to be embedded.

    """
    return incident_horizontal_bar_chart.return_fatality_bar_chart(value).to_html()


@app.callback(Output('jitter_bar_chart', 'srcDoc'),
              [Input('dd_incident_selection', 'value')])
def render_jitter_bar_fatality_chart(value):
    """
     renders the incident jitter/boxplot depending on the selection of the drop-down menus.

    Parameters
    ----------
    value: the dropdown value selected. one of

    Returns
    -------

    """
    return jitter_bar_fatality_chart.return_jitter_bar_fatality_chart(value).to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
