"""
ETL Pipeline DAG - API to Database with Spark Transformation

This DAG orchestrates a complete ETL process:
1. Extract: Fetch data from NYC Open Data API
2. Transform: Clean and transform data using PySpark
3. Load: Store transformed data into PostgreSQL database

Author: Data Engineering Team
"""

from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG
import os
import sys
import logging

# Add parent directory to path for importing custom modules
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_folder)

from spark_jobs.extract_data import extract_from_api
from spark_jobs.transform_data import get_spark_session, transform_with_spark

# Configure logging
logger = logging.getLogger(__name__)

# Default arguments for all tasks
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': 5,  # seconds
}


def extract_and_load_to_staging(**context):
    """
    EXTRACT & LOAD Task: Extract data from API and load into staging table
    
    This task:
    1. Calls the API to fetch data
    2. Creates staging table if it doesn't exist
    3. Inserts raw data into staging.example table
    
    Args:
        **context: Airflow context dictionary
    """
    try:
        logger.info("Starting Extract task: Fetching data from API...")
        
        # Get PostgreSQL connection hook
        postgres_hook = PostgresHook(postgres_conn_id="postgres_conn")
        
        # Extract data from API (returns DataFrame and CREATE TABLE SQL)
        df, create_table_sql = extract_from_api()
        logger.info(f"Successfully extracted {len(df)} records from API")
        
        # Create staging table if it doesn't exist
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        logger.info("Staging table created/verified: staging.example")
        
        # Insert data into staging table
        if len(df) > 0:
            rows = list(df.itertuples(index=False, name=None))
            postgres_hook.insert_rows(table="staging.example", rows=rows)
            logger.info(f"Successfully inserted {len(rows)} rows into staging.example")
        else:
            logger.warning("No data to insert into staging table")
        
        cursor.close()
        conn.close()
        
        logger.info("Extract task completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Extract task: {str(e)}")
        raise


def transform_and_load_to_production(**context):
    """
    TRANSFORM & LOAD Task: Transform data using Spark and load into production table
    
    This task:
    1. Reads data from staging table
    2. Transforms data using PySpark (deduplication, text cleaning)
    3. Creates production table if it doesn't exist
    4. Inserts transformed data into public.example table
    
    Args:
        **context: Airflow context dictionary
    """
    spark = None
    try:
        logger.info("Starting Transform task: Reading from staging table...")
        
        # Get PostgreSQL connection hook
        postgres_hook = PostgresHook(postgres_conn_id="postgres_conn")
        
        # Read data from staging table
        df_staging = postgres_hook.get_pandas_df(sql="SELECT * FROM staging.example")
        logger.info(f"Read {len(df_staging)} records from staging.example")
        
        if len(df_staging) == 0:
            logger.warning("No data in staging table to transform")
            return
        
        # Initialize Spark session
        spark = get_spark_session()
        logger.info("Spark session created")
        
        # Transform data using Spark
        df_transformed = transform_with_spark(spark=spark, df=df_staging)
        logger.info(f"Transformed {len(df_transformed)} records")
        
        # Create production table SQL
        create_prod_sql = """
        CREATE TABLE IF NOT EXISTS public.example (
            fiscal_year INTEGER NULL,
            title_description VARCHAR(200) NULL,
            regular_hours FLOAT NULL,
            regular_gross_paid FLOAT NULL
        );
        """
        
        # Create production table if it doesn't exist
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(create_prod_sql)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Production table created/verified: public.example")
        
        # Insert transformed data into production table
        if len(df_transformed) > 0:
            rows = list(df_transformed.itertuples(index=False, name=None))
            postgres_hook.insert_rows(table="public.example", rows=rows)
            logger.info(f"Successfully inserted {len(rows)} rows into public.example")
        
        logger.info("Transform task completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Transform task: {str(e)}")
        raise
    finally:
        # Always stop Spark session to free resources
        if spark:
            spark.stop()
            logger.info("Spark session stopped")


# Define the DAG
with DAG(
    dag_id="etl_api_to_postgres_pipeline",
    default_args=default_args,
    description="ETL Pipeline: Extract from API, Transform with Spark, Load to PostgreSQL",
    schedule_interval="@daily",  # Runs once per day
    start_date=days_ago(1),  # Start from 1 day ago
    catchup=False,  # Don't run for past dates
    tags=['etl', 'api', 'spark', 'postgres'],
) as dag:
    
    # Start task - marks the beginning of the pipeline
    start_task = EmptyOperator(
        task_id='start',
        doc_md="Start of ETL pipeline"
    )
    
    # Extract task - Fetch data from API and load to staging
    extract_task = PythonOperator(
        task_id='extract_and_load_to_staging',
        python_callable=extract_and_load_to_staging,
        doc_md="Extract data from NYC Open Data API and load into staging table"
    )
    
    # Transform task - Transform data using Spark and load to production
    transform_task = PythonOperator(
        task_id='transform_and_load_to_production',
        python_callable=transform_and_load_to_production,
        doc_md="Transform data using PySpark and load into production table"
    )
    
    # End task - marks the end of the pipeline
    end_task = EmptyOperator(
        task_id='end',
        doc_md="End of ETL pipeline"
    )
    
    # Define task dependencies: start -> extract -> transform -> end
    start_task >> extract_task >> transform_task >> end_task
