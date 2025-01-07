import oracledb
import json

# Load JSON configuration from a file
with open('db_config.json', 'r') as file:
    config_dict = json.load(file)

# Accessing the "info" section
db_info = config_dict["info"]

# Create the Oracle DSN
dsn = f"{db_info['hostname']}:{db_info['port']}/{db_info['servicename']}"

# Establish the Oracle database connection using the JSON data
try:
    # Check if passwordless connection is set
    if db_info["nopasswordconnection"].lower() == "true":
        conn = oracledb.connect(
            dsn=dsn
        )
    else:
        conn = oracledb.connect(
            user=db_info["proxy_user_name"] if db_info["proxy_user_name"] else "myuser",
            password=db_info["password"],
            dsn=dsn
        )
        
    print(f"Connected successfully to {config_dict['name']}")

except oracledb.DatabaseError as e:
    print(f"Error: {e}")

finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")
