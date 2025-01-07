import json
import cx_Oracle
import os
from typing import Optional


class OracleDBConnection:
    def __init__(self, config_path: str):
        """
        Initialize database connection using JSON config file
        
        Args:
            config_path (str): Path to JSON configuration file
        """
        self.config = self._load_config(config_path)
        self.connection = None
        
    def _load_config(self, config_path: str) -> dict:
        """Load and validate database configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            required_keys = ['username', 'password', 'host', 'port', 'service_name']
            if not all(key in config for key in required_keys):
                raise ValueError(f"Config file must contain all required keys: {required_keys}")
                
            return config
    
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at: {config_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in config file")
            
    def connect(self) -> None:
        """Establish connection to Oracle database"""
        try:
            dsn = cx_Oracle.makedsn(
                host=self.config['host'],
                port=self.config['port'],
                service_name=self.config['service_name']
            )
            
            self.connection = cx_Oracle.connect(
                user=self.config['username'],
                password=self.config['password'],
                dsn=dsn
            )
            print("Successfully connected to Oracle database")
            
        except cx_Oracle.Error as error:
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
            
        except cx_Oracle.Error as error:
            raise Exception(f"Error executing query: {error}")

    def __enter__(self):
        """Context manager enter"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
