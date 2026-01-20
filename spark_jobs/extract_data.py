"""
Data Extraction Module

This module handles data extraction from external APIs.
Extracts data from NYC Open Data API and returns it as a pandas DataFrame.

Author: Data Engineering Team
"""

import requests
import pandas as pd
import logging

# Configure logging
logger = logging.getLogger(__name__)


def extract_from_api():
    """
    Extract data from NYC Open Data API
    
    This function:
    1. Makes a GET request to the NYC Open Data API
    2. Converts JSON response to pandas DataFrame
    3. Selects required columns
    4. Returns DataFrame and CREATE TABLE SQL script
    
    Returns:
        tuple: (DataFrame with selected columns, CREATE TABLE SQL string)
        
    Raises:
        Exception: If API request fails or required columns are missing
    """
    try:
        # NYC Open Data API endpoint for payroll data
        api_url = "https://data.cityofnewyork.us/resource/k397-673e.json"
        
        logger.info(f"Fetching data from API: {api_url}")
        
        # Make GET request to API
        response = requests.get(api_url, timeout=30)
        
        # Check if request was successful
        if response.status_code != 200:
            error_msg = f"API request failed with status code: {response.status_code}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Parse JSON response
        data = response.json()
        logger.info(f"Received {len(data)} records from API")
        
        if not data:
            logger.warning("API returned empty response")
            return pd.DataFrame(), get_create_table_sql()
        
        # Convert JSON to pandas DataFrame
        df = pd.DataFrame(data)
        logger.info(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        
        # Required columns from the API response
        required_columns = ["fiscal_year", "title_description", "regular_hours", "regular_gross_paid"]
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            error_msg = f"Missing required columns: {missing_columns}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Select only required columns
        df_selected = df[required_columns].copy()
        
        # Log data types for debugging
        logger.info(f"DataFrame columns: {list(df_selected.columns)}")
        logger.info(f"DataFrame shape: {df_selected.shape}")
        
        # Generate CREATE TABLE SQL script for staging table
        create_table_sql = get_create_table_sql()
        
        return df_selected, create_table_sql
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching data: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error extracting data from API: {str(e)}")
        raise


def get_create_table_sql():
    """
    Generate CREATE TABLE SQL script for staging table
    
    Returns:
        str: SQL CREATE TABLE statement
    """
    return """
    CREATE SCHEMA IF NOT EXISTS staging;
    
    CREATE TABLE IF NOT EXISTS staging.example (
        fiscal_year INTEGER NULL,
        title_description VARCHAR(200) NULL,
        regular_hours FLOAT NULL,
        regular_gross_paid FLOAT NULL
    );
    """


if __name__ == '__main__':
    # Test the extraction function
    logging.basicConfig(level=logging.INFO)
    try:
        df, sql = extract_from_api()
        print(f"Successfully extracted {len(df)} records")
        print(f"Columns: {list(df.columns)}")
        print("\nSample data:")
        print(df.head())
    except Exception as e:
        print(f"Error: {str(e)}")
