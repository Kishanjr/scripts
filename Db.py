import json
import oracledb
import re
from typing import Optional, Dict


class OracleCustomConnection:
    def __init__(self, config_json: Dict):
        """
        Initialize database connection using custom JSON config format
        
        Args:
            config_json (Dict): Configuration dictionary
        """
        self.config = config_json.get('info', {})
        self.connection = None
        self.connection_params = self._parse_jdbc_url()
        
    def _parse_jdbc_url(self) -> Dict[str, str]:
        """Parse JDBC URL to extract connection parameters"""
        jdbc_url = self.config.get('customusrl', '')
        
        # Extract connection details from JDBC URL using regex
        pattern = r"@\(description=\(address\s*=\s*\(protocol\s*=\s*tcp\)\(host\s*=\s*([^)]+)\)"
        host_match = re.search(pattern, jdbc_url.lower())
        
        connection_params = {
            'host': host_match.group(1) if host_match else None,
            'user': self.config.get('user', ''),
            'password': self.config.get('password', ''),
            'driver_type': self.config.get('oradrivertype', 'thin'),
            'kerberos': self.config.get('kerberos', 'false').lower() == 'true',
            'os_authentication': self.config.get('os_autherntication', '').lower() == 'true'
        }
        
        return connection_params
        
    def connect(self) -> None:
        """Establish connection to Oracle database"""
        try:
            # Handle different authentication methods
            if self.connection_params['os_authentication']:
                # Use OS authentication
                self.connection = oracledb.connect(mode=oracledb.AUTH_MODE_OS)
            
            elif self.connection_params['kerberos']:
                # Use Kerberos authentication
                raise NotImplementedError("Kerberos authentication not implemented in this version")
            
            else:
                # Use regular authentication
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
        """
        Execute SQL query and return results
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            list: Query results
        """
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
