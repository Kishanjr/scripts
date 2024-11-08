import psycopg2
from psycopg2 import OperationalError

def run_query(ordernumber):
    try:
        # Establish the database connection
        connection = psycopg2.connect(
            host="your_host",         # e.g., 'localhost' or database server IP
            database="your_database", # replace with your database name
            user="your_username",     # replace with your username
            password="your_password"  # replace with your password
        )

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query with a placeholder for ordernumber
        query = """
            -- Step the cancel
            SELECT 
                ordernumber,
                task_id,
                taskname,
                status,
                user_id,
                task_type,
                parenttask_name,
                taskgroup_id
            FROM 
                vlocal.task
            WHERE 
                ordernumber = %s
                AND status IN ('READY', 'ACQUIRED')
                -- Uncomment below lines for additional filters
                -- AND taskname = 'IASA Task'
                -- AND taskname = 'CANCEL Order error Check comments'
            ORDER BY 
                1;
        """

        # Execute the query with the provided ordernumber
        cursor.execute(query, (ordernumber,))

        # Fetch and print the results
        records = cursor.fetchall()
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

# Prompt for input and run the query
user_ordernumber = input("Enter the ordernumber: ")
run_query(user_ordernumber)
