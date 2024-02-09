#!/usr/bin/env python3

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

element_heading = html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40})

lauch_sites = list(spacex_df.groupby('Launch Site').size().reset_index()['Launch Site'])
element_dropdown = dcc.Dropdown(
                        id='site-dropdown', 
                        options=[{'label': 'All Sites', 'value': 'ALL'}] + [ {'label': ls, 'value': ls} for ls in lauch_sites ],
                        value='ALL',
                        placeholder="place holder here",
                        searchable=True
                    )

range_slider = dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[0, 10000])

# Create an app layout
app.layout = html.Div(children=[element_heading,element_dropdown, html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                range_slider,

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['class'] == 1]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', color = 'Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        # data = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class').size().reset_index(name='count')
        data = spacex_df[spacex_df['Launch Site'] == entered_site].value_counts('class').reset_index()
        fig = px.pie(data, values='count', names='class', color='class', title=f'Total Success Launches for site {entered_site}')
        return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, payload_range):
    
    if entered_site == 'ALL':
        filtered_data = spacex_df
        sites = 'all Sites'
    else:
        filtered_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        sites = entered_site
        
    data = filtered_data[(filtered_data['Payload Mass (kg)'] >= payload_range[0]) & (filtered_data['Payload Mass (kg)'] <= payload_range[1])]

    fig = px.scatter(data, y='class', x='Payload Mass (kg)', color='Booster Version Category', title=f'Correlation Between Payload and Success for all {sites}')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
    # print(spacex_df)
    
