import pandas as pd
import os

# Path to the Gold layer
GOLD_DATA_PATH = "s3/gold/daily_sales/"

def calculate_monthly_sales(gold_data_path):
    try:
        # Load all Parquet files from the Gold layer
        gold_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(gold_data_path) for f in filenames if f.endswith('.parquet')]

        # Print the files found (optional for debugging)
        # print(gold_files)

        if not gold_files:
            print("No Parquet files found in the Gold layer.")
            return

        # Read the Parquet files into a single DataFrame
        df = pd.concat([pd.read_parquet(file) for file in gold_files], ignore_index=True)

        # Convert the 'sale_date' column to datetime if necessary
        if not pd.api.types.is_datetime64_any_dtype(df['sale_date']):
            df['sale_date'] = pd.to_datetime(df['sale_date'])

        # Create auxiliary columns for year and month
        df['year'] = df['sale_date'].dt.year
        df['month'] = df['sale_date'].dt.month

        # Aggregate by year and month
        monthly_sales = df.groupby(['year', 'month']).agg(
            total_sales=('total_sales', 'sum'),
            total_quantity=('total_quantity', 'sum')
        ).reset_index()

        # Sort the results by year and month
        monthly_sales = monthly_sales.sort_values(by=['year', 'month'])

        print("Monthly sales totals:")
        print(monthly_sales)

        return monthly_sales
    # Capture any exceptions that may occur during processing
    except Exception as e:
        print(f"Error calculating monthly sales: {e}")

# Calculate the total monthly sales
monthly_sales = calculate_monthly_sales(GOLD_DATA_PATH)
