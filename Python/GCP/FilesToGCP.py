from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery
import pandas as pd

# Google Cloud Platform credentials (replace with your own)
GOOGLE_CLOUD_PROJECT_ID = 'your-project-id'
GOOGLE_APPLICATION_CREDENTIALS = '/path/to/your/credentials.json'

# Define your BigQuery dataset and table
BIGQUERY_DATASET_ID = 'your_dataset_id'
BIGQUERY_TABLE_ID = 'your_table_id'

# Function to send data to BigQuery
def send_data_to_bigquery():
    # Create a DataFrame (example)
    data = {'column1': [1, 2, 3, 4, 5],
            'column2': ['a', 'b', 'c', 'd', 'e']}
    df = pd.DataFrame(data)

    # Initialize BigQuery client
    client = bigquery.Client(project=GOOGLE_CLOUD_PROJECT_ID)

    # Define BigQuery dataset and table references
    dataset_ref = client.dataset(BIGQUERY_DATASET_ID)
    table_ref = dataset_ref.table(BIGQUERY_TABLE_ID)

    # Insert data into BigQuery table
    client.insert_rows_from_dataframe(table_ref, df)

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'send_data_to_bigquery',
    default_args=default_args,
    description='A simple DAG to send data to BigQuery',
    schedule_interval=timedelta(days=1),  # Run once a day
)

# Define the task
send_data_task = PythonOperator(
    task_id='send_data_to_bigquery_task',
    python_callable=send_data_to_bigquery,
    dag=dag,
)

# Set task dependencies
send_data_task
