# Importing required packages
from google.cloud import bigquery

# Defining schemas for our 3 tables on BigQuery
# DataFrames that will be loaded into these tables will adhere to their respective schemas

forecast_2hr_schema = [
    bigquery.SchemaField('area', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('latitude', 'FLOAT64', mode='REQUIRED'),
    bigquery.SchemaField('longitude', 'FLOAT64', mode='REQUIRED'),
    bigquery.SchemaField('forecast_2hr', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('fetch_time', 'DATETIME', mode='REQUIRED'),
]

forecast_24hr_general_schema = [
    bigquery.SchemaField('forecast_24hr', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('relative_humidity_low', 'FLOAT64', mode='NULLABLE'),
    bigquery.SchemaField('relative_humidity_high', 'FLOAT64', mode='NULLABLE'),
    bigquery.SchemaField('temperature_low', 'FLOAT64', mode='NULLABLE'),
    bigquery.SchemaField('temperature_high', 'FLOAT64', mode='NULLABLE'),
    bigquery.SchemaField('wind_speed_low', 'FLOAT64', mode='NULLABLE'),
    bigquery.SchemaField('wind_speed_high', 'FLOAT64', mode='NULLABLE'),
    bigquery.SchemaField('fetch_time', 'DATETIME', mode='REQUIRED'),
]

forecast_24hr_region_schema = [
    bigquery.SchemaField('area', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('forecast_24hr', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('fetch_time', 'DATETIME', mode='REQUIRED'),
]