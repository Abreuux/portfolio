from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'retail_etl',
    default_args=default_args,
    description='ETL process for retail analytics',
    schedule_interval='@daily',
    catchup=False,
    tags=['retail', 'etl'],
)

# Task functions
def extract_sales_data(**context):
    """Extract sales data from source"""
    # TODO: Implement actual data extraction
    # This is a placeholder that generates sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    data = {
        'date': dates,
        'product_id': np.random.choice(['P001', 'P002', 'P003'], len(dates)),
        'store_id': np.random.choice(['S001', 'S002', 'S003'], len(dates)),
        'quantity': np.random.randint(1, 100, len(dates)),
        'price': np.random.uniform(10, 1000, len(dates))
    }
    df = pd.DataFrame(data)
    return df

def transform_sales_data(**context):
    """Transform sales data"""
    # Get data from previous task
    ti = context['task_instance']
    df = ti.xcom_pull(task_ids='extract_sales_data')
    
    # Add calculated columns
    df['total_amount'] = df['quantity'] * df['price']
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    
    return df

def load_sales_data(**context):
    """Load transformed data into warehouse"""
    # Get data from previous task
    ti = context['task_instance']
    df = ti.xcom_pull(task_ids='transform_sales_data')
    
    # Connect to PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Load data into warehouse
    # TODO: Implement actual data loading
    print("Loading data into warehouse...")
    print(df.head())

# Task definitions
extract_task = PythonOperator(
    task_id='extract_sales_data',
    python_callable=extract_sales_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_sales_data',
    python_callable=transform_sales_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_sales_data',
    python_callable=load_sales_data,
    provide_context=True,
    dag=dag,
)

# Task dependencies
extract_task >> transform_task >> load_task 