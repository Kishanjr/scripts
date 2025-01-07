import oracledb
import json

# Load the JSON configuration from a file
with open('db_config.json', 'r') as file:
    config_dict = json.load(file)

# Extract the "info" section from the JSON
db_info = config_dict["info"]

# Parse the DSN from the "customurl" field if available
dsn = db_info.get("customurl")

# If DSN is not provided, build it manually using hostname and port (fallback)
if not dsn:
    dsn = f"{db_info['hostname']}:{db_info['port']}/{db_info['servicename']}"

# Attempt to connect using the specified settings
try:
    if db_info["nopasswordconnection"].lower() == "true":
        conn = oracledb.connect(
            user=db_info["user"],
            dsn=dsn
        )
    else:
        conn = oracledb.connect(
            user=db_info["user"],
            password=db_info["password"],
            dsn=dsn
        )

    print(f"Connected successfully to {config_dict['name']}!")

except oracledb.DatabaseError as e:
    print(f"Database connection error: {e}")

finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")
