# Importing required packages
import pandas as pd
from google.cloud import bigquery
import plotly.graph_objects as go
import dash
from dash import dash_table, dcc, html

# Initialising connection to BigQuery
bigquery_client = bigquery.Client()

# Defining the queries to each table
# Project name excluded
table_queries = {
    'forecast_2hr': """
    SELECT * 
    FROM `XXX.weather_forecast.forecast_2hr`
    WHERE EXTRACT(DAYOFYEAR FROM fetch_time) = EXTRACT(DAYOFYEAR FROM CURRENT_DATE())
    ORDER BY area
    """,
    'forecast_24hr_general': """
    SELECT * 
    FROM `XXX.weather_forecast.forecast_24hr_general`
    WHERE EXTRACT(DAYOFYEAR FROM fetch_time) = EXTRACT(DAYOFYEAR FROM CURRENT_DATE())
    """,
    'forecast_24hr_region': """
    SELECT * 
    FROM `XXX.weather_forecast.forecast_24hr_region`
    WHERE EXTRACT(DAYOFYEAR FROM fetch_time) = EXTRACT(DAYOFYEAR FROM CURRENT_DATE())
    ORDER BY area
    """
}


def get_from_bigquery() -> dict:
    """
    Fetches data from BigQuery tables as DataFrame using the queries defined earlier
    :return: Dictionary with table name and DataFrame as key-value pairs
    """
    result = {}
    for table in table_queries.keys():
        dataframe = (
                bigquery_client.query(table_queries[table])
                .result()
                .to_dataframe(create_bqstorage_client=False)
        )
        result[table] = dataframe

    return result


# Fetch data into DataFrames
dict_df = get_from_bigquery()
df_2hr = dict_df['forecast_2hr']
df_24hr_general = dict_df['forecast_24hr_general']
df_24_area = dict_df['forecast_24hr_region']

# Separate forecast in key areas & created new column to display in map
key_areas = ['Changi', 'City', 'Kallang', 'Punggol']
df_key_areas = df_2hr[df_2hr['area'].isin(key_areas)]
df_2hr['text'] = df_2hr['area'] + ": " + df_2hr['forecast_2hr']

# Generating map plot
fig = go.Figure(data=go.Scattermapbox(
    lon=df_2hr['longitude'],
    lat=df_2hr['latitude'],
    text=df_2hr['text'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
))
# Utilising map from Mapbox
fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        # Insert your Mapbox access token here
        accesstoken='XXX',
        bearing=0,
        center=dict(
            lat=1.3521,
            lon=103.8198
        ),
        pitch=0,
        zoom=10
    ),
)

# Setting stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

# Initialising Dash instance
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Weather Forecast'
# Inserting map plot & DataFrames as DataTable
app.layout = html.Div(children=[
    html.H3(children='Today\'s Weather Forecast'),
    html.Div('2 Hour Forecast by Area'),
    dcc.Graph(
        id='forecast_by_area',
        figure=fig
    ),
    html.Div(children=[
        html.Div('2 Hour Forecast of Selected Areas'),
        dash_table.DataTable(df_key_areas.to_dict('records'), fill_width=False),
        html.Div('General 24 Hour Forecast'),
        dash_table.DataTable(df_24hr_general.to_dict('records'), fill_width=False),
        html.Div('24 Hour Forecast by Region'),
        dash_table.DataTable(df_24_area.to_dict('records'), fill_width=False)
        ]
    ),
    html.A('By: Alif Naufal', href='https://github.com/alif898')
    ]
)

# Additional configurations
server = app.server
app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
