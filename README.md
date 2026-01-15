# ETL Pipeline with Apache Airflow and PySpark

A production-ready, fresher-friendly ETL (Extract, Transform, Load) pipeline project demonstrating how to build end-to-end data pipelines using Apache Airflow for orchestration and PySpark for data transformation.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Pipeline](#running-the-pipeline)
- [Expected Output](#expected-output)
- [Common Errors & Fixes](#common-errors--fixes)
- [Interview Tips](#interview-tips)

---

## 🎯 Project Overview

This project demonstrates a complete ETL pipeline that:

1. **Extracts** data from NYC Open Data API (payroll information)
2. **Transforms** the data using PySpark (deduplication, text cleaning)
3. **Loads** the transformed data into PostgreSQL database

The pipeline is orchestrated by Apache Airflow, which schedules and monitors the entire process.

### Why This Project?

- **Real-world Scenario**: Uses actual public API data
- **Complete ETL Flow**: Shows all three phases clearly
- **Production Patterns**: Includes error handling, logging, and best practices
- **Interview Ready**: Clean code with clear explanations

---

## 🛠 Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Orchestration** | Apache Airflow | 2.7.1 | Workflow scheduling and monitoring |
| **Processing** | Apache Spark (PySpark) | 3.5.0 | Distributed data transformation |
| **Database** | PostgreSQL | 14+ | Data storage |
| **Language** | Python | 3.8+ | Development language |
| **Data Processing** | Pandas | 2.0.3 | Data manipulation |
| **Container** | Docker | Latest | PostgreSQL containerization |

---

## 🏗 Architecture

### High-Level Architecture

```
┌─────────────────┐
│  NYC Open Data  │
│      API        │
└────────┬────────┘
         │
         │ Extract
         ▼
┌─────────────────┐
│  Apache Airflow │
│      DAG        │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌──────────────┐
│  Staging Table  │  │   PySpark    │
│ (staging.example)│  │ Transformation│
└────────┬────────┘  └──────┬───────┘
         │                  │
         │                  │
         └──────────┬───────┘
                    │
                    │ Transform & Load
                    ▼
         ┌──────────────────┐
         │ Production Table │
         │ (public.example) │
         └──────────────────┘
```

### Pipeline Flow

1. **Extract Task**: 
   - Fetches data from NYC Open Data API
   - Creates staging schema/table if not exists
   - Loads raw data into `staging.example` table

2. **Transform Task**:
   - Reads data from staging table
   - Uses PySpark to:
     - Remove duplicate records
     - Clean text columns (lowercase → proper case → trim)
     - Keep numeric columns unchanged
   - Creates production schema/table if not exists
   - Loads transformed data into `public.example` table

---

## 📁 Project Structure

```
Airflow-Spark-End-to-End-Basic-Project/
│
├── dags/                          # Airflow DAG definitions
│   ├── __init__.py
│   └── dag.py                    # Main ETL pipeline DAG
│
├── spark_jobs/                    # PySpark transformation scripts
│   ├── __init__.py
│   ├── extract_data.py           # API extraction logic
│   └── transform_data.py         # Spark transformation logic
│
├── data/                          # Data directories
│   ├── raw/                      # Raw data files (if saved locally)
│   └── processed/                # Processed data files
│
├── scripts/                       # Utility scripts
│
├── env/                           # Environment configuration
│   └── postgres.env              # PostgreSQL credentials
│
├── docker-compose.yml            # Docker setup for PostgreSQL
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.8+** installed
- **Java 8 or 11** installed (required for Spark)
- **Docker Desktop** installed (for PostgreSQL)
- **Apache Airflow** installed or ready to install
- **PostgreSQL client** (optional, for manual database inspection)

### Verify Prerequisites

```bash
# Check Python version
python --version

# Check Java version
java -version

# Check Docker
docker --version
```

---

## 🚀 Setup Instructions

### Step 1: Clone and Navigate to Project

```bash
cd Airflow-Spark-End-to-End-Basic-Project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Airflow installation may take a few minutes as it has many dependencies.

### Step 4: Setup PostgreSQL Database

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL container
docker-compose up -d

# Verify container is running
docker ps
```

The PostgreSQL database will be available at:
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: Check `env/postgres.env` file
- **Username/Password**: Check `env/postgres.env` file

#### Option B: Local PostgreSQL

If you have PostgreSQL installed locally, create a database and update connection settings.

### Step 5: Configure Airflow

#### 5.1 Initialize Airflow Database

```bash
# Set AIRFLOW_HOME (optional, defaults to ~/airflow)
export AIRFLOW_HOME=$(pwd)/airflow_home

# Initialize Airflow database
airflow db init
```

#### 5.2 Create Airflow User

```bash
# Create admin user (replace with your credentials)
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

When prompted, enter a password for the admin user.

#### 5.3 Configure PostgreSQL Connection in Airflow

1. Start Airflow webserver:
```bash
airflow webserver --port 8080
```

2. Open browser: `http://localhost:8080`
3. Login with the admin credentials created above
4. Go to **Admin → Connections**
5. Click **+** to add new connection:
   - **Connection Id**: `postgres_conn`
   - **Connection Type**: `Postgres`
   - **Host**: `localhost`
   - **Schema**: `postgres` (or your database name)
   - **Login**: Check `env/postgres.env`
   - **Password**: Check `env/postgres.env`
   - **Port**: `5432`
6. Click **Save**

#### 5.4 Set Airflow DAGs Folder

Make sure your `dags/` folder is in the Airflow DAGs directory, or update `airflow.cfg`:

```bash
# In airflow.cfg, set:
dags_folder = /path/to/your/project/dags
```

Or set environment variable:
```bash
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags
```

### Step 6: Verify Setup

```bash
# Test if DAG is loaded
airflow dags list

# You should see: etl_api_to_postgres_pipeline
```

---

## ▶️ Running the Pipeline

### Method 1: Using Airflow UI (Recommended)

1. **Start Airflow Components**:

```bash
# Terminal 1: Start Airflow webserver
airflow webserver --port 8080

# Terminal 2: Start Airflow scheduler
airflow scheduler
```

2. **Access Airflow UI**: Open `http://localhost:8080` in your browser

3. **Trigger the DAG**:
   - Find `etl_api_to_postgres_pipeline` in the DAG list
   - Toggle it ON (switch on the left)
   - Click the **Play** button to trigger a run
   - Click on the DAG name to see the graph view

4. **Monitor Execution**:
   - Green = Success
   - Red = Failed
   - Orange = Running
   - Click on a task to view logs

### Method 2: Using Airflow CLI

```bash
# Trigger the DAG
airflow dags trigger etl_api_to_postgres_pipeline

# Check status
airflow dags state etl_api_to_postgres_pipeline <execution_date>
```

### Method 3: Test Individual Components

#### Test API Extraction

```bash
cd spark_jobs
python extract_data.py
```

#### Test Spark Transformation

```bash
cd spark_jobs
python transform_data.py
```

---

## 📊 Expected Output

### Database Tables

After running the pipeline, you should see:

#### 1. Staging Table (`staging.example`)

Raw data from API:
- `fiscal_year`: INTEGER
- `title_description`: VARCHAR(200) - Original text
- `regular_hours`: FLOAT
- `regular_gross_paid`: FLOAT

#### 2. Production Table (`public.example`)

Transformed data:
- Same columns as staging
- `title_description`: Cleaned (proper case, trimmed)
- Duplicates removed

### Query to Verify

```sql
-- Connect to PostgreSQL
psql -h localhost -U <username> -d <database>

-- Check staging data
SELECT COUNT(*) FROM staging.example;
SELECT * FROM staging.example LIMIT 5;

-- Check production data (should have cleaned text)
SELECT COUNT(*) FROM public.example;
SELECT * FROM public.example LIMIT 5;

-- Compare transformation (text should be cleaned)
SELECT 
    s.title_description AS staging_text,
    p.title_description AS production_text
FROM staging.example s
JOIN public.example p ON s.fiscal_year = p.fiscal_year
LIMIT 10;
```

---

## ❗ Common Errors & Fixes

### Error 1: "ModuleNotFoundError: No module named 'spark_jobs'"

**Cause**: Python path not set correctly

**Fix**:
```bash
# Make sure you're in the project root directory
# The DAG file should be able to find spark_jobs/ folder
# Check that spark_jobs/__init__.py exists
```

### Error 2: "Connection refused" when connecting to PostgreSQL

**Cause**: PostgreSQL not running or wrong connection details

**Fix**:
```bash
# Check if Docker container is running
docker ps

# If not, start it
docker-compose up -d

# Verify connection settings in Airflow UI (Admin → Connections)
```

### Error 3: "Java not found" or Spark initialization fails

**Cause**: Java not installed or JAVA_HOME not set

**Fix**:
```bash
# Install Java 8 or 11
# On Windows: Download from Oracle or use OpenJDK
# On Mac: brew install openjdk@11
# On Linux: sudo apt-get install openjdk-11-jdk

# Set JAVA_HOME environment variable
export JAVA_HOME=/path/to/java
```

### Error 4: "DAG not showing in Airflow UI"

**Cause**: DAG folder not configured correctly

**Fix**:
```bash
# Check dags_folder in airflow.cfg
# Or set environment variable:
export AIRFLOW__CORE__DAGS_FOLDER=/full/path/to/dags

# Restart Airflow webserver and scheduler
```

### Error 5: "API request failed" or timeout

**Cause**: Network issue or API unavailable

**Fix**:
- Check internet connection
- Verify API URL is accessible: `https://data.cityofnewyork.us/resource/k397-673e.json`
- Check API rate limits
- Add retry logic (already included in code)

### Error 6: "Column not found" error

**Cause**: API response structure changed

**Fix**:
- Check current API response structure
- Update column names in `spark_jobs/extract_data.py` if needed

### Error 7: Airflow tasks keep retrying

**Cause**: Dependencies not installed or configuration issues

**Fix**:
- Check task logs in Airflow UI for specific error
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python path and module imports

---

## 💡 Interview Tips

When explaining this project in interviews, focus on:

### 1. **ETL Process Understanding**
- **Extract**: How you fetch data from external sources (API)
- **Transform**: Why transformations are needed (data quality, consistency)
- **Load**: How data is stored (staging vs production)

### 2. **Key Concepts to Mention**

- **Data Quality**: Deduplication, text cleaning
- **Staging vs Production**: Why we use staging tables
- **Idempotency**: Pipeline can run multiple times safely
- **Error Handling**: Try-except blocks, logging
- **Scalability**: PySpark for large datasets

### 3. **Technical Decisions**

- **Why Airflow?**: Workflow orchestration, monitoring, retry logic
- **Why Spark?**: Distributed processing, handles large datasets
- **Why Staging Tables?**: Data validation before production
- **Why PostgreSQL?**: Relational database, ACID compliance

### 4. **Common Interview Questions**

**Q: How would you handle failures?**
- A: Retry logic in Airflow, error logging, monitoring alerts

**Q: How would you scale this?**
- A: Move Spark to cluster mode, use distributed databases, partition data

**Q: How would you improve data quality?**
- A: Add validation rules, schema checks, data profiling

**Q: What if the API changes?**
- A: Version API responses, add schema validation, alert on schema changes

### 5. **Code Walkthrough**

Be ready to explain:
- DAG structure and task dependencies
- Spark transformations and why they're needed
- Error handling approach
- How you ensured code is production-ready

---

## 🔄 Next Steps / Enhancements

To extend this project, consider:

1. **Add Data Validation**: Schema validation, data quality checks
2. **Incremental Loading**: Track last processed date, only process new data
3. **Monitoring**: Add alerts for failures, data quality metrics
4. **Testing**: Unit tests for each component
5. **Documentation**: API documentation, data dictionary
6. **CI/CD**: Automated testing and deployment
7. **Data Partitioning**: Partition tables by date
8. **Add More Sources**: Multiple API endpoints, databases

---

## 📝 License

This project is for educational purposes.

---

## 👥 Author

Data Engineering Team

**For Questions or Issues**: Open an issue in the repository

---

## 🙏 Acknowledgments

- NYC Open Data for providing the API
- Apache Airflow and Spark communities
- All contributors to open-source data engineering tools

---

**Happy Data Engineering! 🚀**
