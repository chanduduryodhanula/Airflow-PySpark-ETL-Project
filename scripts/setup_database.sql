-- Database Setup Script for ETL Pipeline
-- This script creates the necessary schemas and tables
-- Run this if you want to manually set up the database structure

-- Create staging schema
CREATE SCHEMA IF NOT EXISTS staging;

-- Create staging table (raw data from API)
CREATE TABLE IF NOT EXISTS staging.example (
    fiscal_year INTEGER NULL,
    title_description VARCHAR(200) NULL,
    regular_hours FLOAT NULL,
    regular_gross_paid FLOAT NULL
);

-- Create production schema (if using different schema)
-- By default, we use 'public' schema for production

-- Create production table (transformed data)
CREATE TABLE IF NOT EXISTS public.example (
    fiscal_year INTEGER NULL,
    title_description VARCHAR(200) NULL,
    regular_hours FLOAT NULL,
    regular_gross_paid FLOAT NULL
);

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON SCHEMA staging TO your_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO your_user;

-- Verification queries (uncomment to run)
-- SELECT * FROM staging.example LIMIT 5;
-- SELECT * FROM public.example LIMIT 5;
