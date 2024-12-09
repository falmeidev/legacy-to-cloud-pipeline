import psycopg2
import os
import csv
from config import DB_CONFIG

# Directory that simulates the local S3 bucket
RAW_DATA_DIR = "s3/raw"

# Function to ensure the RAW directory exists
def ensure_raw_directory_exists():
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)
        print(f"Directory created: {RAW_DATA_DIR}")
    else:
        print(f"Directory already exists: {RAW_DATA_DIR}")

# Function to extract data from PostgreSQL and save as a CSV file
def export_data_to_raw():
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        # Create a cursor to execute SQL commands on the database
        cursor = conn.cursor()

        # SQL query to extract all data from the 'sales' table
        query = "SELECT * FROM sales;"
        # Execute the query on the database
        cursor.execute(query)
        # Retrieve a list of tuples, where each tuple is a row from the table
        rows = cursor.fetchall()
        # Get column names from the queried table
        # 'cursor.description' contains metadata about the columns returned by the query
        columns = [desc[0] for desc in cursor.description]
        
        # Define the path for the CSV file in the RAW layer
        # 'RAW_DATA_DIR' should be defined earlier in the code and points to the RAW directory in the file system
        raw_file_path = os.path.join(RAW_DATA_DIR, "sales_raw.csv")
        # Open a CSV file for writing at the defined path
        # 'newline=""' avoids extra blank lines on some systems
        # 'encoding="utf-8"' ensures compatibility with special characters
        with open(raw_file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)  # Create a CSV writer object
            writer.writerow(columns)  # Write the header to the file (column names)
            writer.writerows(rows)    # Write the extracted data to the file
        # Print a success message indicating the data export
        print(f"Data successfully exported to: {raw_file_path}")

    # Exception handling to capture errors during execution
    except Exception as e:
        print(f"Error exporting data: {e}")

    # Finally block to ensure resources are closed even in case of error
    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

ensure_raw_directory_exists()  # Ensure the RAW directory exists
export_data_to_raw()           # Export data to the RAW directory
