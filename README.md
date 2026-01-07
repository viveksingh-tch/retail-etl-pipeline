# 🛒 Automated Retail ETL Pipeline

## 📖 Project Overview
This project is an end-to-end Data Engineering pipeline designed to automate the processing of daily retail sales data. 

It simulates a real-world enterprise environment where raw transaction logs are:
1.  **Ingested** from a source system.
2.  **Cleaned & Transformed** using Python and Pandas (applying business logic).
3.  **Loaded** into a Data Warehouse (DuckDB) for analytics.
4.  **Orchestrated** fully automatically using **Apache Airflow**.

## 🏗️ Architecture Diagram
*(This pipeline follows the standard ETL pattern)*

```mermaid
graph LR
    A[Source: Sales System] -->|Generates Daily CSV| B(Landing Zone)
    B -->|Trigger| C{Apache Airflow DAG}
    C -->|Task 1: Extract| D[Python Script: Generate Data]
    C -->|Task 2: Transform & Load| E[Python Script: Clean & Insert]
    E -->|Final Storage| F[(DuckDB Data Warehouse)]

🛠️ Tech Stack
Orchestration: Apache Airflow 2.9

Language: Python 3.10+

Transformation: Pandas (DataFrames)

Data Warehouse: DuckDB (Serverless SQL OLAP database)

Infrastructure: Docker & GitHub Codespaces (Linux/Ubuntu Environment)

⚡ Key Features
Automated Workflow: The pipeline runs on a daily schedule without manual intervention.

Data Quality Checks: Automatically filters out low-value transactions (Business Rule: Orders < $50 are discarded).

Idempotency: Designed to handle retries without creating duplicate data or crashing.

Local Development: Fully containerized environment that mimics production cloud setups.

🚀 How to Run This Project
If you want to run this locally, follow these steps:

1. Clone the Repository
Bash

git clone [https://github.com/YOUR_GITHUB_USERNAME/retail-etl-pipeline.git](https://github.com/YOUR_GITHUB_USERNAME/retail-etl-pipeline.git)
cd retail-etl-pipeline
2. Set Up Environment
Bash

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install pandas duckdb faker apache-airflow
3. Start Airflow
Bash

# Initialize Airflow DB
airflow db migrate
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin

# Start Scheduler & Webserver
airflow scheduler & 
airflow webserver -p 8080

4. Verify Data
Once the pipeline runs, you can query the data warehouse directly:
Bash
python -c "import duckdb; print(duckdb.connect('data/retail_wh.duckdb').sql('SELECT * FROM sales LIMIT 5'))"