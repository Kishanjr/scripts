import psycopg2

def update_jsonb_psycopg2(entity_id, spec_name, spec_value, entity_attributes):
    """
    Update a JSONB field in PostgreSQL using psycopg2 with parameter binding.
    """

    # Your PostgreSQL Query with parameterized placeholders
    query = """
    WITH updated_json AS (
        SELECT entity_id, jsonb_agg(
            CASE 
                WHEN elem->>'specName' = %s 
                THEN jsonb_set(elem, '{specValue}', %s::jsonb)
                ELSE elem
            END
        ) as updated_attributevalue
        FROM svcinv.t_service_inventory, jsonb_array_elements(entity_attributes->'entityAttributes') as elem
        WHERE entity_id = %s AND entity_type = 'LOCATION'
        GROUP BY entity_id
    )
    UPDATE svcinv.t_service_inventory tni
    SET entity_attributes = jsonb_set(entity_attributes, '{entityAttributes}', updated_json.updated_attributevalue)
    FROM updated_json
    WHERE tni.entity_id = updated_json.entity_id;
    """

    # Establish database connection and execute the query
    try:
        conn = psycopg2.connect(
            host="localhost",  # Change this
            database="your_database",  # Change this
            user="your_username",  # Change this
            password="your_password"  # Change this
        )
        cur = conn.cursor()

        # Execute the query using safe parameter binding
        cur.execute(query, (spec_name, f'"{spec_value}"', entity_id))

        # Commit the transaction
        conn.commit()
        print("✅ JSONB update successful!")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error occurred: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()


# Example Call
update_jsonb_psycopg2("12345", "ROUTER_SIZE", "5", "entityAttributes")
