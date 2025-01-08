import oracledb
from base64 import b64decode
from Cryptodome.Cipher import DES
from Cryptodome.Hash import MD5

# Hardcoded connection details
username = "your_username"
encrypted_password = "your_encrypted_password"  # The encrypted password from JSON
custom_url = "jdbc:oracle:thin:@(description=(address=(protocol=tcp)(host=your_host)...))"  # Your full custom URL

# Decrypt password (using SQL Developer's default key "123456")
hash_obj = MD5.new("123456".encode('utf-8'))
des_key = hash_obj.digest()[:8]
encrypted_bytes = b64decode(encrypted_password.strip())
cipher = DES.new(des_key, DES.MODE_ECB)
decrypted = cipher.decrypt(encrypted_bytes)
padding_length = decrypted[-1]
password = decrypted[:-padding_length].decode('utf-8')

# Remove JDBC prefix from custom URL if present
dsn = custom_url.replace('jdbc:oracle:thin:@', '')

# Create the connection
try:
    connection = oracledb.connect(
        user=username,
        password=password,  # Using the decrypted password
        dsn=dsn
    )
    
    print("Connected successfully!")
    
    # Test the connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM dual")
    results = cursor.fetchall()
    print(results)
    
    # Close connections
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Error: {e}")
