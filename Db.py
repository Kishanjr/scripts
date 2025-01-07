import cx_Oracle
import json

# Load JSON configuration
with open('db_config.json', 'r') as file:
    config = json.load(file)

# Oracle connection string using TNS
dsn = cx_Oracle.makedsn(config["host"], config["port"], service_name=config["service_name"])

# Establish the database connection with encryption settings
try:
    conn = cx_Oracle.connect(
        user=config["user"],
        password=config["password"],
        dsn=dsn,
        encoding="UTF-8",
        config_dir="./",  # Optional if sqlnet.ora is in a different directory
        mode=cx_Oracle.SYSDBA
    )
    print("Connected successfully with encryption!")

    # Set encryption at session level (if required)
    with conn.cursor() as cursor:
        cursor.execute(f"ALTER SESSION SET encryption = '{config['encryption']}'")
        cursor.execute(f"ALTER SESSION SET encryption_algorithm = '{config['encryption_algorithm']}'")

except cx_Oracle.DatabaseError as e:
    print(f"Error: {e}")

finally:
    if conn:
        conn.close()
        print("Connection closed.")
