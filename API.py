from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

def update_automation_audit(data):
    """
    Updates or inserts a record in the automation_audit table.
    :param data: Dictionary containing the data for each column
    """
    try:
        # Establish the database connection
        connection = psycopg2.connect(
            host="localhost",         # Adjust if necessary
            database="test_db",       # Use the test database
            user="your_username",     # Replace with your PostgreSQL username
            password="your_password"  # Replace with your PostgreSQL password
        )

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query to update the automation_audit table
        update_query = """
            INSERT INTO automation_audit (entity_type, entity_value, ticket, channel, description, vast_id, updated_time)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (entity_value) DO UPDATE SET
                entity_type = EXCLUDED.entity_type,
                ticket = EXCLUDED.ticket,
                channel = EXCLUDED.channel,
                description = EXCLUDED.description,
                vast_id = EXCLUDED.vast_id,
                updated_time = NOW();
        """

        # Execute the query with data from the API request
        cursor.execute(update_query, (
            data.get('entity_type'),
            data.get('entity_value'),
            data.get('ticket'),
            data.get('channel'),
            data.get('description'),
            data.get('vast_id')
        ))

        # Commit the transaction
        connection.commit()

        return {"message": "Record updated successfully."}

    except OperationalError as e:
        return {"error": f"Database connection error: {e}"}

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()

@app.route('/update_audit', methods=['POST'])
def update_audit():
    data = request.get_json()

    # Validate required fields
    required_fields = ['entity_type', 'entity_value', 'ticket', 'channel', 'description', 'vast_id']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Update the database
    response = update_automation_audit(data)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
