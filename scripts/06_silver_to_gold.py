import pandas as pd
import os
import glob

# Define paths for Silver and Gold layers
SILVER_DATA_PATH = "s3/silver/sales_silver"  # Silver layer directory
GOLD_DATA_PATH = "s3/gold/"  # Base directory for the Gold layer

# Ensure the Gold directory exists
def ensure_gold_directory_exists():
    # Check if the path defined in 'GOLD_DATA_PATH' exists
    if not os.path.exists(GOLD_DATA_PATH):
        # Create the directory if it doesn't exist
        os.makedirs(GOLD_DATA_PATH)
        # Message indicating the directory was created
        print(f"Directory created: {GOLD_DATA_PATH}")
    else:
        # If the directory already exists, display an informational message
        print(f"Directory already exists: {GOLD_DATA_PATH}")

# Process data from the Silver layer and create dimension and fact tables
def process_and_move_to_gold():
    # Find all Parquet files stored in the Silver layer
    silver_files = glob.glob(os.path.join(SILVER_DATA_PATH, "*.parquet"))

    # Check if there are files in the Silver layer
    if not silver_files:
        # Message if no data is found
        print("No Parquet files found in the Silver layer.")
        return  # Exit the function if there are no files to process

    # Load all Parquet files into a single DataFrame using pandas
    sales_data = pd.concat([pd.read_parquet(file) for file in silver_files], ignore_index=True)
    print(f"Data loaded from Silver layer. Total rows: {len(sales_data)}")

    # **Creating Dimensions**
    # Product Dimension: Unique list of products (IDs)
    dim_product = sales_data[['product_id']].drop_duplicates().reset_index(drop=True)
    # Customer Dimension: Combine customer with their region, removing duplicates
    dim_customer = sales_data[['customer_id', 'region']].drop_duplicates().reset_index(drop=True)
    # Seller Dimension: Unique list of seller IDs
    dim_seller = sales_data[['seller_id']].drop_duplicates().reset_index(drop=True)
    # Date Dimension: Unique list of dates with additional attributes (year, month, day)
    dim_date = sales_data[['sale_date']].drop_duplicates().reset_index(drop=True)
    dim_date['year'] = pd.to_datetime(dim_date['sale_date']).dt.year  # Extract year
    dim_date['month'] = pd.to_datetime(dim_date['sale_date']).dt.month  # Extract month
    dim_date['day'] = pd.to_datetime(dim_date['sale_date']).dt.day  # Extract day

    # **Creating Fact Table**
    # Contains transactional sales information (dimension keys and metrics)
    fact_sales = sales_data[['sale_date', 'product_id', 'customer_id', 'seller_id', 'quantity', 'total_value']]

    # **Daily Aggregation**
    # Group sales by date and calculate metrics like total sales and total quantity
    daily_sales = fact_sales.groupby('sale_date').agg(
        total_sales=('total_value', 'sum'),
        total_quantity=('quantity', 'sum')
    ).reset_index()

    # **Save Dimensions and Fact Tables to the Gold Layer**
    # Each dimension and fact table is saved as a separate Parquet file in the Gold layer
    dim_product.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_product.parquet"), index=False)
    dim_customer.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_customer.parquet"), index=False)
    dim_seller.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_seller.parquet"), index=False)
    dim_date.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_date.parquet"), index=False)
    fact_sales.to_parquet(os.path.join(GOLD_DATA_PATH, "fact_sales.parquet"), index=False)

    # **Partitioning Daily Sales**
    # Add partition columns (year, month, day) to organize the data
    daily_sales['sale_date'] = pd.to_datetime(daily_sales['sale_date'])
    daily_sales['year'] = daily_sales['sale_date'].dt.year
    daily_sales['month'] = daily_sales['sale_date'].dt.month
    daily_sales['day'] = daily_sales['sale_date'].dt.day

    # Define the path to save daily sales in the Gold layer
    gold_daily_sales_path = os.path.join(GOLD_DATA_PATH, "daily_sales/")
    # Ensure the directory for partitioned daily sales exists
    if not os.path.exists(gold_daily_sales_path):
        os.makedirs(gold_daily_sales_path)
    # Save the data partitioned by year/month/day in Parquet format
    daily_sales.to_parquet(gold_daily_sales_path, index=False, partition_cols=['year', 'month', 'day'])

    # Success message after processing
    print("Data processed and saved to the Gold layer successfully.")


ensure_gold_directory_exists()  # Ensure the Gold directory exists
process_and_move_to_gold()  # Execute the Silver → Gold pipeline
