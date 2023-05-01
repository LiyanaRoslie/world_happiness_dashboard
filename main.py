import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

happiness=pd.read_csv('world_happiness.csv')

region_options=[{'label': i, 'value': i} for i in happiness['region'].unique()]

country_options=[{'label': i, 'value': i} for i in happiness['country'].unique()]

line_fig=px.line(happiness[happiness['country']=='United States'],x='year', y='happiness_score', title='Happiness Score in the USA')

app=dash.Dash()

app.layout = html.Div([
    # can remove children=
    #html.H1(children="World Happiness Dashboard"),

    html.H1("World Happiness Dashboard"),
    html.P(['This dashboard shows the happiness score',
            html.Br(),
            html.A('World Happiness Report Data Source',
                   href='https://worldhappiness.report/',
                   target='_blank')]),
    #dcc.RadioItems(options=region_options, value='North America'),
    #dcc.Checklist(options=region_options, value=['North America']),
    dcc.Dropdown(id='country-dropdown', options=country_options, value='United States'),
    #manipulate using pandas dataframe
    dcc.Graph(id='happiness-graph')
])

@app.callback(
    #shortform
    #Output('happiness-graph', 'figure'),
    #Input('country-dropdown', 'value')
    Output(component_id='happiness-graph', component_property='figure'),
    Input(component_id='country-dropdown', component_property='value')
)
def update_graph(selected_country):
    filtered_happiness = happiness[happiness['country']==selected_country]
    line_fig=px.line(filtered_happiness, x='year', y='happiness_score',
                     title=f'Happiness Score in {selected_country}')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)