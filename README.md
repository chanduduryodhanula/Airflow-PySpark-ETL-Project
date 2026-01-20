# ETL Pipeline using Apache Airflow and PySpark

This project shows how to build a basic ETL pipeline using Apache Airflow and PySpark.
The pipeline takes data from an API, cleans it, and stores it in a database.

This project is created to understand real-world data engineering concepts in a simple way.

---

## What this Project Does

The ETL pipeline performs three steps:

1. Extract data from NYC Open Data API  
2. Transform the data using PySpark  
3. Load the cleaned data into PostgreSQL  

Apache Airflow is used to schedule and monitor the pipeline.

---

## Why I Built This Project

- To learn how ETL pipelines work end to end  
- To understand Apache Airflow and DAGs  
- To practice PySpark for data processing  
- To work with real API data  
- To explain a data engineering project clearly in interviews  

---

## Tools Used

- Apache Airflow – workflow scheduling  
- PySpark – data transformation  
- PostgreSQL – data storage  
- Python – programming language  
- Docker – PostgreSQL container  

---

## Pipeline Flow

NYC Open Data API
↓
Airflow DAG
↓
Staging Table (PostgreSQL)
↓
PySpark Transformation
↓
Final Table (PostgreSQL)

---

## How the Pipeline Works

### Extract
- Data is fetched from NYC Open Data API  
- Raw data is stored in a staging table  
- No data cleaning is done at this stage  

### Transform
- Data is read from the staging table  
- PySpark is used to:
  - Remove duplicate records  
  - Clean text columns  
  - Keep numeric columns unchanged  

### Load
- Cleaned data is saved into a production table  
- This table is used for final analysis  

---

## Project Structure

Airflow-Spark-End-to-End-Basic-Project/
│
├── dags/
│ └── dag.py
│
├── spark_jobs/
│ ├── extract_data.py
│ └── transform_data.py
│
├── env/
│ └── postgres.env
│
├── docker-compose.yml
├── requirements.txt
└── README.md


---

## Requirements

- Python 3.8+
- Java 8 or 11
- Docker
- Apache Airflow

---

## How to Run the Project

1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate

2.Install dependencies
pip install -r requirements.txt

3.Start PostgreSQL
docker-compose up -d

4.Initialize Airflow
airflow db init

5.Start Airflow
airflow webserver
airflow scheduler

6.Open browser
http://localhost:8080

7.Enable and trigger the DAG
Output

Staging table contains raw API data

Final table contains cleaned and deduplicated data

Interview Explanation (Simple)

“I built an ETL pipeline using Airflow and PySpark.
Data is extracted from an API, stored in a staging table, cleaned using Spark, and loaded into PostgreSQL.
Airflow controls the workflow and handles retries.”

What I Learned

End-to-end ETL process

Airflow DAGs and scheduling

Spark-based data cleaning

Importance of staging tables

Future Improvements

Incremental data loading

Data validation checks

Alerts for pipeline failures
