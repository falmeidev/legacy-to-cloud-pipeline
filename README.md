# Legacy to Cloud Pipeline

This project implements a complete pipeline to migrate data from a legacy system to a modern architecture based on AWS. The structure follows the data layering pattern (RAW, BRONZE, SILVER, GOLD) and uses various AWS services for storage, transformation, and analysis.

---

## 🎯 Objective

Migrate and modernize the data infrastructure of a legacy system, enabling:
- Greater scalability and efficiency.
- Structuring data for advanced analyses.
- Automation of ETL processes.

---

## 🗂️ Project Structure

Below is the organization of the project's folders and files:

- **`docs/`**: Additional and detailed documentation about the project.
- **`resources/`**: Support files, such as configurations and templates.
- **`s3/`**:
  - **`raw/`**: Raw data extracted from the legacy system.
  - **`bronze/`**: Structured and cleaned data.
  - **`silver/`**: Enriched data ready for analysis.
  - **`gold/`**: Final data optimized for analytical consumption and dashboards.
- **`scripts/`**:
  - `01_create_db.py`: Script to create the legacy database.
  - `02_create_and_populate_tb.py`: Populates tables in the legacy database.
  - `03_export_to_raw.py`: Exports data to the RAW layer in S3.
  - `04_raw_to_bronze.py`: Transforms data from the RAW layer to BRONZE.
  - `05_bronze_to_silver.py`: Processes data from the BRONZE layer to SILVER.
  - `06_silver_to_gold.py`: Enriches and transforms data from the SILVER layer to GOLD.
  - `07_sales_months_analysis.py`: Monthly sales analysis for dashboards.
  - `config.py`: Configuration file for connections and global variables.
  - `sales_vs_month.sql`: SQL query for sales analysis by month.
- **`.gitignore`**: Configuration to ignore irrelevant files and folders in versioning.
---

## 🚀 How to Set Up and Run

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-user/legacy-to-cloud-pipeline.git
   cd legacy-to-cloud-pipeline

2. **Run the scripts in order**:

- Create and populate the legacy database:
    ```
    python scripts/01_create_db.py
    python scripts/02_create_and_populate_tb.py
    ```

- Export data and process layers:
    ```
    python scripts/03_export_to_raw.py
    python scripts/04_raw_to_bronze.py
    python scripts/05_bronze_to_silver.py
    python scripts/06_silver_to_gold.py
    ```
- Generate sales reports:
    ```
    python scripts/07_sales_months_analysis.py
    ```

## 📊 Project Benefits

- **Infrastructure Modernization**
Transition from legacy systems to scalable cloud services, increasing operational efficiency.

- **Automation**
Automated data pipelines eliminate manual tasks, saving time and reducing errors.

- **Scalability and Flexibility**
The architecture supports high data volumes and advanced analyses, and is ready for future integrations, such as predictive models and real-time analyses.

## 📋 License

This project is licensed under the terms of the MIT License.