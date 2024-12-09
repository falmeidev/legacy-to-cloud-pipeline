import psycopg2
from config import DB_CONFIG

# Function to create the 'legacy_sales_db' database if it doesn't already exist
def create_database():
    try:
        # Connects to the PostgreSQL server using the configurations defined in 'DB_CONFIG'
        # 'DB_CONFIG' should contain details like host, user, password, and port.
        conn = psycopg2.connect(**DB_CONFIG)
        # Enables autocommit mode, required to execute commands like CREATE DATABASE.
        # Without autocommit, the command would be part of a transaction, which is not allowed for CREATE DATABASE.
        conn.autocommit = True  
        # Creates a cursor to execute SQL commands on the PostgreSQL server.
        cursor = conn.cursor()
        
        # Checks if the 'legacy_sales_db' database already exists.
        # The SELECT 1 query returns a row if the database exists; otherwise, it returns nothing.
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'legacy_sales_db'")
        # If the cursor does not return any result, it means the database does not exist.
        if not cursor.fetchone():
            # Creates the 'legacy_sales_db' database if it does not exist.
            cursor.execute("CREATE DATABASE legacy_sales_db")
            print("Database 'legacy_sales_db' created successfully.")
        else:
            # Informs that the database already exists and does not need to be created.
            print("Database 'legacy_sales_db' already exists.")

    # Captures any exception that may occur during the connection or execution of commands.    
    except Exception as e:
        print("Error creating the database:", e)
    
    # The 'finally' block is used to ensure that resources are properly released,
    # regardless of success or failure in the 'try' block.
    finally:
        if cursor:  # Checks if the cursor was initialized
            cursor.close() # Closes the cursor to release resources
        if conn:  # Checks if the connection was established
            conn.close() # Closes the connection to the database

# Executes the create_database function
create_database()
