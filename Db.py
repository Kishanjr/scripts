import json
import oracledb
import re
from typing import Optional, Dict
from base64 import b64encode, b64decode
from Crypto.Cipher import DES
from Crypto.Hash import MD5
import binascii


class SQLDeveloperPasswordDecryption:
    def __init__(self, key: str = "123456"):
        """
        Initialize decryption with SQL Developer compatible key
        
        Args:
            key (str): Decryption key (default is SQL Developer's "123456")
        """
        self.key = self._prepare_key(key)
    
    def _prepare_key(self, key: str) -> bytes:
        """Prepare the key using MD5 hash like SQL Developer"""
        hash_obj = MD5.new(key.encode('utf-8'))
        return hash_obj.digest()[:8]  # DES key must be 8 bytes
    
    def decrypt_password(self, encrypted_password: str) -> str:
        """
        Decrypt SQL Developer encrypted password
        
        Args:
            encrypted_password (str): Base64 encoded encrypted password
            
        Returns:
            str: Decrypted password
        """
        try:
            # Remove any whitespace and decode base64
            encrypted_bytes = b64decode(encrypted_password.strip())
            
            # Create DES cipher object
            cipher = DES.new(self.key, DES.MODE_ECB)
            
            # Decrypt and remove padding
            decrypted = cipher.decrypt(encrypted_bytes)
            
            # Remove PKCS5 padding
            padding_length = decrypted[-1]
            decrypted = decrypted[:-padding_length]
            
            return decrypted.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Failed to decrypt password: {e}")


class OracleCustomConnection:
    def __init__(self, config_json: Dict, key: str = "123456"):
        """
        Initialize database connection using custom JSON config format
        
        Args:
            config_json (Dict): Configuration dictionary
            key (str): Key for password decryption (default SQL Developer key)
        """
        self.config = config_json.get('info', {})
        self.password_handler = SQLDeveloperPasswordDecryption(key)
        self.connection_params = self._parse_jdbc_url()
        self.connection = None
        
    def _parse_jdbc_url(self) -> Dict[str, str]:
        """Parse JDBC URL to extract connection parameters"""
        jdbc_url = self.config.get('customusrl', '')
        
        # Extract connection details from JDBC URL using regex
        pattern = r"@\(description=\(address\s*=\s*\(protocol\s*=\s*tcp\)\(host\s*=\s*([^)]+)\)"
        host_match = re.search(pattern, jdbc_url.lower())
        
        # Get password and decrypt
        password = self.config.get('password', '')
        if password:
            try:
                password = self.password_handler.decrypt_password(password)
            except ValueError as e:
                print(f"Warning: Could not decrypt password: {e}")
                password = ''  # Clear password on decryption failure
        
        connection_params = {
            'host': host_match.group(1) if host_match else None,
            'user': self.config.get('user', ''),
            'password': password,
            'driver_type': self.config.get('oradrivertype', 'thin'),
            'kerberos': self.config.get('kerberos', 'false').lower() == 'true',
            'os_authentication': self.config.get('os_autherntication', '').lower() == 'true'
        }
        
        return connection_params
        
    def connect(self) -> None:
        """Establish connection to Oracle database"""
        try:
            if self.connection_params['os_authentication']:
                self.connection = oracledb.connect(mode=oracledb.AUTH_MODE_OS)
            
            elif self.connection_params['kerberos']:
                raise NotImplementedError("Kerberos authentication not implemented in this version")
            
            else:
                if not self.config.get('customusrl'):
                    raise ValueError("Custom URL is required for database connection")
                
                # For thick mode (uncomment if needed)
                # oracledb.init_oracle_client()
                
                self.connection = oracledb.connect(
                    user=self.connection_params['user'],
                    password=self.connection_params['password'],
                    dsn=self.config['customusrl'].replace('jdbc:oracle:thin:@', '')
                )
                
            print("Successfully connected to Oracle database")
            
        except oracledb.Error as error:
            raise Exception(f"Error connecting to Oracle database: {error}")
            
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
            
    def execute_query(self, query: str) -> list:
        """Execute SQL query and return results"""
        if not self.connection:
            raise Exception("No active database connection")
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
            
        except oracledb.Error as error:
            raise Exception(f"Error executing query: {error}")
            
    def __enter__(self):
        """Context manager enter"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
