from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

# Database connection function
def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="your_username",       # Replace with your PostgreSQL username
        password="your_password"     # Replace with your PostgreSQL password
    )
    return connection

# POST method - Create or update a record
@app.route('/update_audit', methods=['POST'])
def update_audit():
    data = request.get_json()

    required_fields = ['entity_type', 'entity_value', 'ticket', 'channel', 'description', 'vast_id']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
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
        cursor.execute(query, (
            data['entity_type'],
            data['entity_value'],
            data['ticket'],
            data['channel'],
            data['description'],
            data['vast_id']
        ))
        connection.commit()
        return jsonify({"message": "Record added/updated successfully."})

    except OperationalError as e:
        return jsonify({"error": f"Database connection error: {e}"})

    finally:
        cursor.close()
        connection.close()

# GET method - Retrieve records
@app.route('/audit', methods=['GET'])
def get_audit():
    entity_value = request.args.get('entity_value')
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        if entity_value:
            query = "SELECT * FROM automation_audit WHERE entity_value = %s"
            cursor.execute(query, (entity_value,))
        else:
            query = "SELECT * FROM automation_audit"
            cursor.execute(query)

        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in records]

        return jsonify(results)

    except OperationalError as e:
        return jsonify({"error": f"Database connection error: {e}"})

    finally:
        cursor.close()
        connection.close()

# PUT method - Update specific fields of an existing record
@app.route('/audit', methods=['PUT'])
def put_audit():
    data = request.get_json()
    entity_value = data.get('entity_value')

    if not entity_value:
        return jsonify({"error": "Missing 'entity_value' in request body"}), 400

    fields_to_update = {key: data[key] for key in data if key != 'entity_value'}
    if not fields_to_update:
        return jsonify({"error": "No fields to update provided"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        set_clause = ", ".join([f"{key} = %s" for key in fields_to_update.keys()])
        values = list(fields_to_update.values()) + [entity_value]

        query = f"UPDATE automation_audit SET {set_clause}, updated_time = NOW() WHERE entity_value = %s"
        cursor.execute(query, values)
        connection.commit()

        return jsonify({"message": "Record updated successfully"})

    except OperationalError as e:
        return jsonify({"error": f"Database connection error: {e}"})

    finally:
        cursor.close()
        connection.close()

# DELETE method - Delete a record
@app.route('/audit', methods=['DELETE'])
def delete_audit():
    entity_value = request.args.get('entity_value')

    if not entity_value:
        return jsonify({"error": "Missing 'entity_value' in request parameters"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM automation_audit WHERE entity_value = %s"
        cursor.execute(query, (entity_value,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Record not found"}), 404
        else:
            return jsonify({"message": "Record deleted successfully"})

    except OperationalError as e:
        return jsonify({"error": f"Database connection error: {e}"})

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
