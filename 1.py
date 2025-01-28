import psycopg2
from psycopg2.extras import execute_values

# Database connection
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="your_host",
    port="your_port"
)
cursor = conn.cursor()

# Accept multiple orders as input
orders = []
while True:
    entity_type = input("Enter entity_type (or 'exit' to finish): ")
    if entity_type.lower() == 'exit':
        break
    ticket = input("Enter ticket: ")
    channel = input("Enter channel: ")
    description = input("Enter description: ")
    vast_id = input("Enter vast_id: ")
    entity_value = input("Enter entity_value: ")

    # Append as tuple
    orders.append((entity_type, ticket, channel, description, vast_id, entity_value, "2024-12-23 07:25:00"))

# If there are orders, insert them in bulk
if orders:
    query = """
    INSERT INTO synapt_dev_db.usecase_metrics (
        entity_type, ticket, channel, description, vast_id, entity_value, updated_time
    )
    VALUES %s
    ON CONFLICT (entity_type, ticket, channel, description, vast_id)
    DO UPDATE SET 
        entity_value = EXCLUDED.entity_value,
        updated_time = EXCLUDED.updated_time;
    """
    
    # Use execute_values for bulk insertion
    execute_values(cursor, query, orders)
    conn.commit()

    print(f"{len(orders)} records inserted/updated successfully.")

# Close the connection
cursor.close()
conn.close()
