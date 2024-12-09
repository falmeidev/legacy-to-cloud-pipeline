import psycopg2
from datetime import datetime, timedelta
import random
from config import DB_CONFIG

# Function to generate fake sales data
def generate_sales_data(num_records=500):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    products = list(range(101, 111))
    regions = ['North', 'South', 'East', 'West', 'Center']
    
    sales_data = []
    for _ in range(num_records):
        sale_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        product_id = random.choice(products)
        customer_id = random.randint(1001, 2000)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10.0, 100.0), 2)
        total_value = round(quantity * unit_price, 2)
        seller_id = random.randint(1, 20)
        region = random.choice(regions)
        
        sale = (sale_date.strftime('%Y-%m-%d'), product_id, customer_id, quantity, unit_price, total_value, seller_id, region)
        sales_data.append(sale)
    return sales_data

# Function to create the table and insert data
def create_and_insert_sales():
    conn = None  # Initializes the connection variable
    cursor = None  # Initializes the cursor variable
    try:
        # Connect to the PostgreSQL database using the settings stored in DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # SQL command to create the 'sales' table if it doesn't already exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            sale_date DATE NOT NULL,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_value DECIMAL(10,2) NOT NULL,
            seller_id INTEGER NOT NULL,
            region VARCHAR(50) NOT NULL
        );
        """
        # Executes the SQL command to create the table
        cursor.execute(create_table_query)
        # Confirms the table creation in the database
        conn.commit()
        print("Table 'sales' created successfully.")
        
        # Generates fake data to insert into the table
        sales_data = generate_sales_data(500)
        
        # Insert the generated data
        insert_query = """
        INSERT INTO sales (sale_date, product_id, customer_id, quantity, unit_price, total_value, seller_id, region)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Inserts the generated data into the table using executemany, which allows multiple inserts in a single operation
        cursor.executemany(insert_query, sales_data)
        # Confirms the data insertion in the database
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")
    
    # Exception handling to capture errors during execution
    except Exception as e:
        # Displays the error message
        print("Error:", e)
    
    # Finally block to ensure resources are closed even in case of an error
    finally:
        # Close the cursor and connection if they were created
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Calls the function to create the table and insert data
create_and_insert_sales()
