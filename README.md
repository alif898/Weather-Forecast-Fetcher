# Weather-Forecast-Fetcher

## Introduction

I love to cycle during my free time and weather is always something we need to check before heading out.
Unfortuantely I can be a bit absent-minded on this and many times I chose a route that was going to rain, which usually means I have to cut my session short, especially if the rain is too heavy.
Of course, there are many weather related apps and services which can help me with this, but naturally, I was keen to build my own custom solution.

The idea is to find a source of weather forecast data, build an ETL pipeline to take this data, store it somewhere before delivering the weather forecasts in a way that is convenient to me, such as through an email or link that I can access easily. A task orchestration tool will be used to ensure that this entire process is done regularly.

This writeup will cover the following parts:
 1. System design
 2. Instructions on how to use this repo
 3. Conclusion

## System design

For the data source, I discovered that [data.gov.sg](https://data.gov.sg/) has an API that allows us to fetch the 2hr and 24hr forecast data of Singapore, so I will be using that as the data source. The code that handles the logic of making the API request and wrangling the data into a pandas DataFrame is found in [forecast.py](utilities/forecast.py), under utilities.

Next, I was considering how to store the data, as well as how to go about using a task orchestration tool to handle the ETL process. I decided to use this project as an opportunity to familiarise myself with a cloud computing service, in this case, Google Cloud Platform (GCP), due to its relatively generous free tier and trial period.

As such, I decided to go with GCP’s BigQuery as the data storage solution. Although the scale of this project is unlikely to be able to make full use of BigQuery, it is still a learning opportunity for me to familiarise myself with a data warehouse solution. The schema used can be found in [schema.py](utilities/schema.py).

For task orchestration, Apache Airflow is a commonly used tool in the Data Engineering space, in part due to the fact that it is open source. However, it might seem that setting up an instance of Apache Airflow, even locally, can be cumbersome to manage. Conveniently, GCP has a service called Google Cloud Composer, which is a managed instance of Apache Airflow, so I will be using this. The airflow DAG used can be found in [forecast_dag.py](forecast_dag.py)

With Cloud Composer set up, we now have weather forecast data regularly loaded into BigQuery. Now, it is time to figure out how to deliver this data.

To visualise the weather forecast, I decided to use Plotly and Dash. Dash is a framework created by Plotly for interactive web applications. Plotly itself is a well-known data visualisation tool in Python, so I thought this setup will work well. Since Dash can create a web app to display the weather forecast, I decided to use Google Cloud Run to deploy the web app. Again, since the bulk of this project is already on GCP, it will be convenient to use Google Cloud Run. Google Cloud Run is a compute platform that allows us to run and deploy containers, without the hassle of infrastrcuture management.

To summarise, here is a diagram showing the system design of this project.

![diagram](https://github.com/alif898/Weather-Forecast-Fetcher/blob/main/diagram.png?raw=true)

## Instructions on how to use this repo

