import psycopg2

# Database connection setup
connection = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)

cursor = connection.cursor()

# List of tickets to update
ticket_list = [101, 102, 103, 104]  # Replace with your ticket numbers

# Common values for other columns
entity_type = "example_entity_type"
entity_value = "example_entity_value"
channel = "example_channel"
description = "example_description"
vast_id = "example_vast_id"

# Update query
update_query = """
UPDATE synapt_dev_db.usecase_metrics
SET 
    ticket = %s,
    updated_time = NOW()
WHERE 
    entity_type = %s AND
    entity_value = %s AND
    channel = %s AND
    description = %s AND
    vast_id = %s;
"""

# Loop through the tickets and execute the query
try:
    for ticket in ticket_list:
        cursor.execute(update_query, (ticket, entity_type, entity_value, channel, description, vast_id))
    connection.commit()  # Commit the transaction
    print("Tickets updated successfully.")
except Exception as e:
    print(f"Error: {e}")
    connection.rollback()  # Roll back the transaction in case of an error
finally:
    cursor.close()
    connection.close()
