# Data Migration from Legacy System to AWS-based Architecture

## 1 - Creating an AWS RDS Service to Simulate the Legacy Database with PostgreSQL

To simulate the legacy database with sales data, PostgreSQL was chosen due to its robustness and support for advanced features, making it widely used in older transactional database solutions, fitting well in our legacy system scenario.

An RDS (Relational Database Service) instance was created with PostgreSQL as the engine in AWS. This is a quick way to set up a database instance, and the Free Tier can be utilized, allowing free usage for the first 12 months, with some limitations on time and storage capacity (details about the Amazon RDS Free Tier can be found here: [AWS Free Tier](https://aws.amazon.com/pt/free/database/)).

Steps to create the instance:

### 1.1 - In the AWS search bar, type "RDS" and click on the service.

<img src="../resources/imgs/rds_creation_step1.png" alt="Create RDS instance step 1" width="800"/>

### 1.2 - On the RDS resources overview page, click "Create database."

<img src="../resources/imgs/rds_creation_step2.png" alt="Create RDS instance step 2" width="800"/>

### 1.3 - As mentioned, a standard instance will be created with PostgreSQL as the engine.

<img src="../resources/imgs/rds_creation_step3.png" alt="Create RDS instance step 3" width="800"/>

### 1.4 - Select the desired configurations, paying special attention to "Credential Settings" to create a database access password. At the bottom of the page, click "Create database."

<img src="../resources/imgs/rds_creation_step4.png" alt="Create RDS instance step 4" width="800"/>

### 1.5 - After a few minutes, the instance will be created and available.

<img src="../resources/imgs/rds_creation_step5.png" alt="Create RDS instance step 5" width="800"/>

---

## 2 - Data Ingestion into PostgreSQL

To ingest data into the created database, two Python scripts will be used. The first, `01_create_db.py`, will create the "legacy_sales_db" database if it doesn't exist. The second script, `02_create_and_populate_tb.py`, will create the "sales" table and insert sales data (500 records). These scripts are located in the `scripts/` folder.

Database access credentials (host, port, username, password, etc.) are imported from a separate `config.py` file, which is listed in `.gitignore`. This is a good practice to avoid sharing sensitive information in the repository.

After running these two scripts, the data will be inserted into PostgreSQL.

<img src="../resources/imgs/data_ingestion_step1.png" alt="Data ingestion step 1" width="800"/>

**IMPORTANT**: *To view the data in the PostgreSQL instance, the DBeaver client application was used. It supports SQL and NoSQL databases. Download it here: [DBeaver Download](https://dbeaver.io/download/).*

---

## 3 - Data Migration to RAW Layer

For this project, S3 buckets were simulated in a local directory called `s3`.

The Medallion Architecture was used for data organization in S3 to enhance governance, traceability, and auditability. It is particularly effective in collaborative environments where different teams work with various data layers (raw, transformed, aggregated, etc.). Additionally, it is ideal for scalable, reliable, and organized data handling.

<img src="../resources/imgs/medallion_architecture.png" alt="Medallion Architecture" width="800"/>

The layers are as follows:
1. **RAW**: Stores original data in CSV format.
2. **BRONZE**: Copies RAW data partitioned by year, month, and day, saved in Parquet format.
3. **SILVER**: Cleans and enriches the data (e.g., ISO date format conversion, duplicate removal).
4. **GOLD**: Implements dimensional modeling (**fact and dimension tables**) and aggregates daily sales data.

The script `03_export_to_raw.py` was used to migrate data from PostgreSQL to the RAW layer. This script queries the relational database and writes the data in CSV format to the `s3/raw` directory, simulating S3 ingestion.

**IMPORTANT**: *This project includes four folders within `s3` for each layer. In a real S3 implementation, each layer could either be a separate bucket or folders within a single bucket.*

Data movement from RDS to the RAW layer is illustrated below:

<img src="../resources/imgs/rds_to_raw.png" alt="RDS to RAW" width="600"/>

---

## 4 - Migration from RAW to BRONZE Layer

Data in the BRONZE layer is identical to RAW but partitioned by year, month, and day. This is implemented in the Python script `04_raw_to_bronze.py`.

The script reads RAW data, partitions it, and saves it in Parquet format in the BRONZE layer, improving query performance and scalability.

<img src="../resources/imgs/partition_bronze_layer.png" alt="Partition Bronze Layer" width="600"/>

The resulting project structure is shown below:

<img src="../resources/imgs/raw_to_bronze.png" alt="RAW to BRONZE" width="600"/>

---

## 5 - Migration from BRONZE to SILVER Layer

Per the Medallion Architecture, data in the SILVER layer is cleaned and enriched. The Python script `05_bronze_to_silver.py` converts dates to ISO format (YYYY-MM-DD, more info: [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)) and removes duplicates.

The SILVER layer often serves as an intermediate step for analytical processing, so the data is consolidated into a single Parquet file (`sales.parquet`).

<img src="../resources/imgs/silver_layer.png" alt="Silver Layer" width="600"/>

The resulting project structure is shown below:

<img src="../resources/imgs/bronze_to_silver.png" alt="BRONZE to SILVER" width="600"/>

---

## 6 - Migration from SILVER to GOLD Layer

The GOLD layer involves two processes:
1. Dimensional modeling:
   - `dim_customer.parquet`
   - `dim_date.parquet`
   - `dim_product.parquet`
   - `dim_seller.parquet`
   - `fact_sales.parquet`
2. Aggregating daily sales data (total sales value and quantity), partitioned by year, month, and day, saved in Parquet format.

Both processes are implemented in `06_silver_to_gold.py`.

The resulting project structure is shown below:

<img src="../resources/imgs/silver_to_gold.png" alt="SILVER to GOLD" width="600"/>

---

## 7 - Daily Sales Analysis

The script `07_sales_months_analysis.py` summarizes daily sales data from the GOLD layer into monthly aggregates. Results are displayed as follows:

<img src="../resources/imgs/monthly_sales.png" alt="Monthly Sales" width="300"/>

---

## 8 - SQL Queries in Athena

To query S3 tables in Athena:
1. Configure a Glue Crawler to detect file schemas and register them in the Glue Data Catalog (dimensional tables only).
2. Use Athena for SQL queries and enable AWS CloudWatch Logs for monitoring, integrating with SNS for notifications.

A sample query is available in `scripts/monthly_sales.sql`.

---

## 9 - Alignment with Modern AWS Architecture

This project can be implemented using only AWS services. The architecture includes:
- RDS for the legacy database (PostgreSQL engine).
- CDC tools (e.g., DMS) or Glue ETL for data migration to S3.
- Glue Crawler for schema discovery and Data Catalog registration.
- Athena for SQL querying.
- QuickSight for dashboards.

The diagram below illustrates the architecture:

<img src="../resources/imgs/aws_native_services.png" alt="AWS Native Services" width="800"/>

---

## 10 - Machine Learning Proposal with SageMaker

A proposal was developed for predictive sales modeling using Amazon SageMaker. The goal is to forecast future sales for inventory planning, resource allocation, and marketing optimization. Data from the GOLD layer, including historical sales, product categories, regions, and seasonality, will be used.

Details are available in `docs/ml_proposal.md`.
