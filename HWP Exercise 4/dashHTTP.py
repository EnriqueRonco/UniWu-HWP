from fileinput import filename
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

app = Dash(__name__)

pathway = "data" # Path where the CSV files are relative to the Dash file
files = [os.path.join(pathway, f) for f in os.listdir(pathway) if os.path.isfile(os.path.join(pathway, f))]

app.layout = html.Div([
    html.H4('Temperature graphs of the different dates'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in files
    ], # Dropdown menu with the different files
    multi=False
    ),
    dcc.Graph(id="graph"),
    dcc.Interval(
        id='interval-component',
        interval=5000,
        n_intervals=0
    ) # Update interval time of 5s
])

@app.callback(
    Output("graph", "figure"), [Input("dropdown", "value"), Input("interval-component", "n_intervals") ]
)
def display_graph(dropdown, n_intervals):
    if dropdown is not None:
        df = pd.read_csv(dropdown) # Read the CSV file

        # Convert the date from Epoch to Datetime, convert it into Berlin's Timezone
        df['Date'] = pd.to_datetime(df['Date'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Europe/Berlin')
        
        # Plot the temperature relative to the time
        fig = px.line(df, x = 'Date', y = 'Temperature')
        return fig
    else:
        return {} # If no CSV file is found, return empty

app.run_server(debug=True)