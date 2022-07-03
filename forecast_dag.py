# Importing required packages
import datetime
import logging

# Importing forecast getters & schemas
from utilities.forecast import get_2hr_forecast, get_24hr_forecast_general, get_24hr_forecast_region
from utilities.schema import forecast_2hr_schema, forecast_24hr_general_schema, forecast_24hr_region_schema

# Importing Airflow & GCP packages
from airflow import models
from airflow.operators import python
from airflow.operators.email import EmailOperator
from google.cloud import bigquery

# Fetching GCP Project ID and setting Dataset ID & Table IDs
project_id = models.Variable.get('gcp-project-id')
dataset_id = 'weather_forecast'
table_ids = [
    'forecast_2hr',
    'forecast_24hr_general',
    'forecast_24hr_region'
]
# Initialise BigQuery client
bigquery_client = bigquery.Client()

# Define yesterday for default_dag_args
yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

# Setting default DAG arguments
default_dag_args = {
    'start_date': yesterday,
    'email': models.Variable.get('email'),
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': project_id
}

# Creating DAG, set to run every day at midnight UTC time
with models.DAG(
        'forecast_getter',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args
) as dag:

    # Defining the 3 python callables that trigger the load job for BigQuery
    # Uses the imported schemas and functions that handle the API call -> JSON -> DataFrame logic

    def load_2hr_forecast() -> None:
        table_id = f"{project_id}.{dataset_id}.{table_ids[0]}"
        job_config = bigquery.LoadJobConfig(
            schema=forecast_2hr_schema
        )
        job = bigquery_client.load_table_from_dataframe(
            get_2hr_forecast(), table_id, job_config=job_config
        )
        logging.info(job.result())

    def load_24hr_forecast_general() -> None:
        table_id = f"{project_id}.{dataset_id}.{table_ids[1]}"
        job_config = bigquery.LoadJobConfig(
            schema=forecast_24hr_general_schema
        )
        job = bigquery_client.load_table_from_dataframe(
            get_24hr_forecast_general(), table_id, job_config=job_config
        )
        logging.info(job.result())

    def load_24hr_forecast_region() -> None:
        table_id = f"{project_id}.{dataset_id}.{table_ids[2]}"
        job_config = bigquery.LoadJobConfig(
            schema=forecast_24hr_region_schema
        )
        job = bigquery_client.load_table_from_dataframe(
            get_24hr_forecast_region(), table_id, job_config=job_config
        )
        logging.info(job.result())

    task_2hr_forecast = python.PythonOperator(
        task_id='task_2hr_forecast',
        python_callable=load_2hr_forecast
    )

    task_24hr_forecast_general = python.PythonOperator(
        task_id='task_24hr_forecast_general',
        python_callable=load_24hr_forecast_general
    )

    task_24hr_forecast_region = python.PythonOperator(
        task_id='task_24hr_forecast_region',
        python_callable=load_24hr_forecast_region
    )

    # Defining task that will send email upon completing the forecast getter tasks
    task_send_email = EmailOperator(
        task_id='task_send_email',
        conn_id='sendgrid_default',
        to='alif898@gmail.com',
        subject='Daily Weather Forecast Update',
        html_content=(
            """
            New weather forecast update complete.
            
            <a href='https://plotly-dash-2qgkppxq3q-as.a.run.app/'>Link</a>
            """
        ),
        dag=dag
    )

    task_2hr_forecast >> task_send_email
    task_24hr_forecast_general >> task_send_email
    task_24hr_forecast_region >> task_send_email
