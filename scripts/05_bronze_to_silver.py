import pandas as pd
import os
import glob

# Define paths for BRONZE and SILVER layers
BRONZE_DATA_PATH = "s3/bronze/sales_bronze/"
SILVER_DATA_PATH = "s3/silver/sales_silver/"

# Ensure the SILVER directory exists
def ensure_silver_directory_exists():
    if not os.path.exists(SILVER_DATA_PATH):
        os.makedirs(SILVER_DATA_PATH)
        print(f"Directory created: {SILVER_DATA_PATH}")
    else:
        print(f"Directory already exists: {SILVER_DATA_PATH}")

# Function to process data: convert dates and remove duplicates
def process_data(df):
    # Convert dates to ISO format (YYYY-MM-DD)
    if 'sale_date' in df.columns:  # Replace 'sale_date' with the name of your date column
        df['sale_date'] = pd.to_datetime(df['sale_date']).dt.strftime('%Y-%m-%d')  # Convert to ISO format
    else:
        raise ValueError("The column 'sale_date' was not found in the dataset.")

    # Remove duplicates
    df = df.drop_duplicates()

    return df

# Function to move data from BRONZE layer to SILVER layer
def bronze_to_silver():
    try:
        # Find all Parquet files in the BRONZE layer
        bronze_files = glob.glob(os.path.join(BRONZE_DATA_PATH, "**/*.parquet"), recursive=True)
        
        if not bronze_files:
            raise FileNotFoundError("No files found in the BRONZE layer.")

        # Initialize the consolidated DataFrame
        processed_data = pd.DataFrame()

        for file in bronze_files:
            print(f"Processing file: {file}")
            
            # Read the Parquet file
            bronze_data = pd.read_parquet(file)

            # Process the data
            processed_data = pd.concat([processed_data, process_data(bronze_data)], ignore_index=True)

        # Save the consolidated DataFrame to the SILVER layer
        processed_data.to_parquet(f'{SILVER_DATA_PATH}/sales.parquet', index=False)
        print(f"Data processed and saved to SILVER layer: {SILVER_DATA_PATH}/sales.parquet")

    except Exception as e:
        print(f"Error moving data to the SILVER layer: {e}")


ensure_silver_directory_exists()  # Ensure the SILVER directory exists
bronze_to_silver()  # Execute the BRONZE → SILVER transformation
