"""
Data Transformation Module

This module handles data transformation using PySpark.
Transforms data by:
1. Removing duplicates
2. Cleaning text columns (lowercase, proper case, trim whitespace)
3. Maintaining numeric columns unchanged

Author: Data Engineering Team
"""

import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, initcap, trim
from pyspark.sql.types import IntegerType, DoubleType, FloatType, LongType, ShortType, ByteType
import logging

# Configure logging
logger = logging.getLogger(__name__)


def get_spark_session():
    """
    Create and return a Spark Session
    
    This function initializes a Spark session with local mode configuration.
    In production, you would typically connect to a Spark cluster.
    
    Returns:
        SparkSession: Configured Spark session
    """
    try:
        logger.info("Initializing Spark session...")
        
        spark = SparkSession.builder \
            .master("local[4]") \
            .appName("ETLDataPipeline") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .getOrCreate()
        
        logger.info("Spark session created successfully")
        return spark
        
    except Exception as e:
        logger.error(f"Error creating Spark session: {str(e)}")
        raise


def transform_with_spark(spark, df):
    """
    Transform data using PySpark
    
    This function:
    1. Converts pandas DataFrame to Spark DataFrame
    2. Caches the DataFrame for better performance
    3. Removes duplicate rows
    4. Cleans text columns (lowercase -> proper case -> trim)
    5. Leaves numeric columns unchanged
    6. Converts back to pandas DataFrame
    
    Args:
        spark (SparkSession): Active Spark session
        df (pandas.DataFrame): Input DataFrame to transform
        
    Returns:
        pandas.DataFrame: Transformed DataFrame
    """
    try:
        logger.info(f"Starting transformation on DataFrame with {len(df)} rows")
        
        # Convert pandas DataFrame to Spark DataFrame
        spark_df = spark.createDataFrame(df)
        logger.info(f"Created Spark DataFrame with {spark_df.count()} rows")
        
        # Cache the DataFrame for multiple operations (improves performance)
        spark_df.cache()
        
        # Remove duplicate rows
        # Note: dropDuplicates() returns a new DataFrame (Spark DataFrames are immutable)
        spark_df = spark_df.dropDuplicates()
        row_count_after_dedup = spark_df.count()
        logger.info(f"After removing duplicates: {row_count_after_dedup} rows")
        
        # Identify numeric and string columns
        numeric_columns = []
        string_columns = []
        
        # Check each column's data type
        for column_name in spark_df.columns:
            column_type = spark_df.schema[column_name].dataType
            
            # Check if column is numeric type
            if isinstance(column_type, (IntegerType, DoubleType, FloatType, LongType, ShortType, ByteType)):
                numeric_columns.append(column_name)
            else:
                # Assume it's a string/text column
                string_columns.append(column_name)
        
        logger.info(f"Numeric columns: {numeric_columns}")
        logger.info(f"String columns: {string_columns}")
        
        # Transform string columns: lowercase -> proper case -> trim whitespace
        # This ensures consistent formatting across all text fields
        for column in string_columns:
            spark_df = spark_df \
                .withColumn(column, lower(col(column))) \
                .withColumn(column, initcap(col(column))) \
                .withColumn(column, trim(col(column)))
        
        logger.info("Text columns transformed: lowercase -> proper case -> trimmed")
        
        # Convert Spark DataFrame back to pandas DataFrame
        # Note: This should be done only if the result fits in memory
        pandas_df = spark_df.toPandas()
        
        # Unpersist cached DataFrame to free memory
        spark_df.unpersist()
        
        logger.info(f"Transformation completed. Final row count: {len(pandas_df)}")
        
        return pandas_df
        
    except Exception as e:
        logger.error(f"Error transforming data with Spark: {str(e)}")
        raise


if __name__ == "__main__":
    # Example usage (for testing purposes)
    logging.basicConfig(level=logging.INFO)
    
    # Note: This main block is for testing only
    # In production, this module is called from Airflow DAG
    try:
        import pandas as pd
        
        # Create sample data for testing
        sample_data = {
            'fiscal_year': [2020, 2021, 2020],
            'title_description': ['  DATA ENGINEER  ', 'software developer', 'DATA ENGINEER'],
            'regular_hours': [40.0, 35.0, 40.0],
            'regular_gross_paid': [5000.0, 4500.0, 5000.0]
        }
        test_df = pd.DataFrame(sample_data)
        
        print("Original DataFrame:")
        print(test_df)
        
        # Test transformation
        spark = get_spark_session()
        transformed_df = transform_with_spark(spark=spark, df=test_df)
        
        print("\nTransformed DataFrame:")
        print(transformed_df)
        
        # Stop Spark session
        spark.stop()
        
    except Exception as e:
        print(f"Error: {str(e)}")
