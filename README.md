# Weather-Forecast-Fetcher

## Introduction

I love to cycle during my free time and weather is always something we need to check before heading out.
Unfortuantely I can be a bit absent-minded on this and many times I chose a route that was going to rain, which usually means I have to cut my session short, especially if the rain is too heavy.
Of course, there are many weather related apps and services which can help me with this, but naturally, I was keen to build my own custom solution.

The idea is to find a source of weather forecast data, build an ETL pipeline to take this data, store it somewhere before delivering the weather forecasts in a way that is convenient to me, such as through an email or link that I can access easily.

This writeup will cover the following parts:
 1. System design
 2. Data visualisation
 3. Instructions on how to use this repo
 4. Conclusion

## System design

For the data source, I discovered that [data.gov.sg](https://data.gov.sg/) has an API that allows us to fetch the 2hr and 24hr forecast data of Singapore, so I will be using that as the data source. The code that handles the logic of making the API request and wrangling the data into a pandas DataFrame is found in [forecast.py](https://github.com/alif898/Weather-Forecast-Fetcher/blob/main/utilities/forecast.py), under utilities.
