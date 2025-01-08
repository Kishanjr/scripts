import oracledb
from base64 import b64decode
from Cryptodome.Cipher import DES
from Cryptodome.Hash import MD5
from Cryptodome.Util.Padding import unpad

def decrypt_password(encrypted_password, key_phrase):
    try:
        # Generate key from phrase
        hash_obj = MD5.new(key_phrase.encode('utf-8'))
        des_key = hash_obj.digest()[:8]
        
        # Decode base64 and decrypt
        encrypted_bytes = b64decode(encrypted_password.strip())
        cipher = DES.new(des_key, DES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted_bytes)
        
        # Proper PKCS7 unpadding
        try:
            unpadded = unpad(decrypted, DES.block_size)
            return unpadded.decode('utf-8')
        except ValueError as e:
            print(f"Padding error: {e}. This might indicate an incorrect key or corrupted data.")
            return None
            
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def connect_to_oracle(username, encrypted_password, custom_url, key_phrase):
    try:
        # Initialize oracle client
        oracledb.init_oracle_client()
        
        # Decrypt password
        password = decrypt_password(encrypted_password, key_phrase)
        if not password:
            raise ValueError("Password decryption failed")
            
        # Process connection string
        dsn = custom_url.replace('jdbc:oracle:thin:@', '')
        
        # Establish connection
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn=dsn
        )
        
        return connection
        
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Usage example
if __name__ == "__main__":
    CONFIG = {
        "username": "your_username",
        "encrypted_password": "your_encrypted_password",
        "custom_url": "jdbc:oracle:thin:@(description=(address=(protocol=tcp)(host=your_host)...))",
        "key_phrase": "123456"
    }
    
    try:
        connection = connect_to_oracle(
            CONFIG["username"],
            CONFIG["encrypted_password"],
            CONFIG["custom_url"],
            CONFIG["key_phrase"]
        )
        
        if connection:
            print("Connected successfully!")
            
            # Test the connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM dual")
                results = cursor.fetchall()
                print(results)
            
            # Close connection
            connection.close()
            
    except Exception as e:
        print(f"Error: {e}")
