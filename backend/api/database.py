import os
import mysql.connector
from mysql.connector import pooling, Error
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "space_station_db"),
    "pool_name": "space_station_pool",
    "pool_size": 5,
    "pool_reset_session": True
}

# Initialize connection pool
try:
    connection_pool = pooling.MySQLConnectionPool(**DB_CONFIG)
except Error as e:
    print(f"Error creating connection pool: {e}")
    connection_pool = None


def get_db_connection():
    """
    Get a database connection from the pool.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection
        
    Raises:
        Exception: If connection cannot be established
    """
    try:
        if connection_pool:
            connection = connection_pool.get_connection()
            if connection.is_connected():
                return connection
        else:
            # Fallback to direct connection if pool is not available
            connection = mysql.connector.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"]
            )
            return connection
    except Error as e:
        raise Exception(f"Error connecting to MySQL database: {e}")


def execute_query(query: str, params: Optional[tuple] = None, fetch: str = "all"):
    """
    Execute a SQL query with error handling.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: "all", "one", or "none" for SELECT queries
        
    Returns:
        Query results or None
        
    Raises:
        Exception: If query execution fails
    """
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch == "all":
            result = cursor.fetchall()
        elif fetch == "one":
            result = cursor.fetchone()
        else:
            result = None
        
        connection.commit()
        return result
        
    except Error as e:
        if connection:
            connection.rollback()
        raise Exception(f"Database query error: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def test_connection():
    """
    Test the database connection.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        connection = get_db_connection()
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_info}")
            connection.close()
            return True
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return False
