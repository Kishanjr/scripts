import oracledb
import json

# Create JSON configuration using json.dumps()
config = json.dumps({
    "host": "localhost",
    "port": "1521",
    "service_name": "orclpdb1",
    "user": "myuser",
    "password": "mypassword",
    "encryption": "REQUIRED",
    "encryption_algorithm": "AES256"
})

# Load the JSON string back as a Python dictionary
config_dict = json.loads(config)

# Create the Oracle DSN (Data Source Name)
dsn = f"{config_dict['host']}:{config_dict['port']}/{config_dict['service_name']}"

# Establish the encrypted Oracle connection
try:
    conn = oracledb.connect(
        user=config_dict["user"],
        password=config_dict["password"],
        dsn=dsn
    )
    print("Connected successfully with encryption!")

    # Set encryption settings at the session level
    with conn.cursor() as cursor:
        cursor.execute(f"ALTER SESSION SET encryption = '{config_dict['encryption']}'")
        cursor.execute(f"ALTER SESSION SET encryption_algorithm = '{config_dict['encryption_algorithm']}'")

except oracledb.DatabaseError as e:
    print(f"Error: {e}")

finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")
