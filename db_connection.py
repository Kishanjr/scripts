import psycopg2
from psycopg2 import sql, OperationalError

def connect_and_query():
    try:
        # Establish the connection
        connection = psycopg2.connect(
            host="your_host",         # e.g., 'localhost' or database server IP
            database="your_database", # replace with your database name
            user="your_username",     # replace with your username
            password="your_password"  # replace with your password
        )

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query
        query = "SELECT * FROM your_table LIMIT 10;"  # Modify query as needed

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        records = cursor.fetchall()

        # Print the results
        for row in records:
            print(row)

    except OperationalError as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Run the function
connect_and_query()
