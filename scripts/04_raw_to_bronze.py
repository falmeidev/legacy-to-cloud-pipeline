import pandas as pd
import os

# Define paths for RAW and BRONZE layers
RAW_DATA_PATH = "s3/raw/sales_raw.csv"  # Path to the RAW file (CSV)
BRONZE_DATA_PATH = "s3/bronze/sales_bronze"  # Base directory for the BRONZE layer (Parquet)

# Ensure the BRONZE directory exists
def ensure_bronze_directory_exists():
    if not os.path.exists(BRONZE_DATA_PATH):
        os.makedirs(BRONZE_DATA_PATH)
        print(f"Directory created: {BRONZE_DATA_PATH}")
    else:
        print(f"Directory already exists: {BRONZE_DATA_PATH}")

# Function to add partitions
def process_data(df):
    # Convert date columns to ISO format and create partitions
    if 'sale_date' in df.columns:  # Replace 'sale_date' with the name of your date column
        df['year'] = pd.to_datetime(df['sale_date']).dt.year  # Create a column for the year
        df['month'] = pd.to_datetime(df['sale_date']).dt.month  # Create a column for the month
        df['day'] = pd.to_datetime(df['sale_date']).dt.day  # Create a column for the day
    else:
        raise ValueError("The column 'sale_date' was not found in the dataset.")

    return df

# Function to convert data from CSV (RAW) to Parquet (BRONZE) with partitions
def raw_to_bronze():
    try:
        # Read the data from the RAW layer (CSV)
        print(f"Reading data from RAW layer: {RAW_DATA_PATH}")
        raw_data = pd.read_csv(RAW_DATA_PATH)

        # Process the data to create partitions
        print("Processing data...")
        processed_data = process_data(raw_data)

        # Save the data to the BRONZE layer as Parquet with partitions
        print(f"Saving data to BRONZE layer (partitioned): {BRONZE_DATA_PATH}")
        processed_data.to_parquet(
            BRONZE_DATA_PATH,  # Base directory
            index=False,
            partition_cols=['year', 'month', 'day']  # Define partitions
        )
        print("Data successfully processed and saved in Parquet format.")
    except Exception as e:
        print(f"Error processing data: {e}")

ensure_bronze_directory_exists()  # Ensure the BRONZE directory exists
raw_to_bronze()  # Execute the RAW → BRONZE conversion
