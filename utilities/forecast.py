# Importing required packages
import requests
import datetime
import pandas as pd


class InternalServerError(Exception):
    """
    Custom exception to handle possible occurrence of no forecasts being uploaded yet on that day
    """
    def __str__(self) -> str:
        return "Internal Server Error occurred, likely due to no forecast available yet on given date"


def get_forecast_helper(hr: int, today: datetime.datetime) -> dict:
    """
    Function that handles the sends the GET request to data.gov.sg API and returns the JSON returned
    :param hr: Type of forecast to fetch, only 2hr and 24hr forecasts available
    :param today: Today's date as a datetime object
    :return: JSON returned from the API call
    """
    if hr not in [2, 24]:
        return {}
    else:
        params = {"date": today.strftime("%Y-%m-%d")}
        address = f'https://api.data.gov.sg/v1/environment/{hr}-hour-weather-forecast'
        forecasts = requests.get(address, params=params).json()

        # Check for case where Internal Server Error might occur
        if 'message' in forecasts:
            if forecasts['message'] == 'Internal Server Error':
                raise InternalServerError

        return forecasts


def get_2hr_forecast() -> pd.DataFrame:
    """
    Handles logic of wrangling and transforming JSON from API call into DataFrame in the appropriate format
    :return: DataFrame containing 2hr forecast data
    """
    today = datetime.datetime.today()
    forecasts = get_forecast_helper(2, today)

    df_area_metadata = pd.DataFrame(forecasts['area_metadata'])
    df_coords = pd.json_normalize(df_area_metadata['label_location'])
    df_area_coords = df_area_metadata.join(df_coords)
    df_area_coords = df_area_coords.rename(
        columns={
            'name': 'area'
        }
    )

    df_forecasts = pd.DataFrame(forecasts['items'][-1]['forecasts'])
    # Record today's date as the date the data was fetched from the API
    df_forecasts['fetch_time'] = today
    df_forecasts = df_forecasts.rename(
        columns={
            'forecast': 'forecast_2hr'
        }
    )

    df_merged = df_area_coords.merge(df_forecasts, how='inner', on='area')
    df_merged = df_merged.drop(columns=['label_location'])

    return df_merged


def get_24hr_forecast_general() -> pd.DataFrame:
    """
    Handles logic of wrangling and transforming JSON from API call into DataFrame in the appropriate format
    :return: DataFrame containing general 24hr forecast data
    """
    today = datetime.datetime.today()
    forecasts = get_forecast_helper(24, today)

    general_forecast = forecasts['items'][-1]['general']
    general_data = {
        'forecast_24hr': [general_forecast['forecast']],
        'relative_humidity_low': [general_forecast['relative_humidity']['low']],
        'relative_humidity_high': [general_forecast['relative_humidity']['high']],
        'temperature_low': [general_forecast['temperature']['low']],
        'temperature_high': [general_forecast['temperature']['high']],
        'wind_speed_low': [general_forecast['wind']['speed']['low']],
        'wind_speed_high': [general_forecast['wind']['speed']['high']]
    }
    df = pd.DataFrame(general_data)
    # Record today's date as the date the data was fetched from the API
    df['fetch_time'] = today

    return df


def get_24hr_forecast_region() -> pd.DataFrame:
    """
    Handles logic of wrangling and transforming JSON from API call into DataFrame in the appropriate format
    :return: DataFrame containing regional 24hr forecast data
    """
    today = datetime.datetime.today()
    forecasts = get_forecast_helper(24, today)

    df = pd.Series(forecasts['items'][-1]['periods'][-1]['regions']).reset_index()
    df = df.rename(
        columns={
            'index': 'area',
            0: 'forecast_24hr'
        }
    )
    # Record today's date as the date the data was fetched from the API
    df['fetch_time'] = today

    return df
