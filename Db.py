import psycopg2
from psycopg2 import sql, OperationalError

# Database connection details
host = "localhost"
user = "your_username"      # Replace with your PostgreSQL username
password = "your_password"  # Replace with your PostgreSQL password

def create_database():
    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database="postgres"  # Connect to the default 'postgres' database to create a new one
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Create a new database
        cursor.execute("CREATE DATABASE test_db;")
        print("Database 'test_db' created successfully.")

    except OperationalError as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection to the default database
        if connection:
            cursor.close()
            connection.close()
            print("Connection to PostgreSQL closed.")

def create_table():
    try:
        # Connect to the newly created test_db
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database="test_db"
        )
        cursor = connection.cursor()

        # Define the table creation SQL query
        create_table_query = """
        CREATE TABLE IF NOT EXISTS automation_audit (
            entity_type VARCHAR(50),
            entity_value VARCHAR(50) UNIQUE,
            ticket VARCHAR(50),
            channel VARCHAR(50),
            description TEXT,
            vast_id VARCHAR(50),
            updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Execute the table creation query
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'automation_audit' created successfully in database 'test_db'.")

    except OperationalError as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection to the test_db
        if connection:
            cursor.close()
            connection.close()
            print("Connection to test_db closed.")

# Run the functions
create_database()
create_table()
