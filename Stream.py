import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

# ------------------------------- #
# DATABASE CONNECTION SETTINGS
# ------------------------------- #
DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",          # Replace with your PostgreSQL username
    "password": "password",      # Replace with your PostgreSQL password
    "database": "mydb",          # Replace with your PostgreSQL database name
    "port": "5432"               # Default PostgreSQL port
}

# Create the SQLAlchemy Engine
engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# ------------------------------- #
# DATABASE CONNECTION FUNCTION
# ------------------------------- #
def get_db_connection():
    try:
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# ------------------------------- #
# USER AUTHENTICATION FUNCTION (Using SQLAlchemy)
# ------------------------------- #
def authenticate_user(username, password):
    conn = get_db_connection()
    if conn:
        try:
            # Using parameterized query to avoid SQL injection
            query = text("SELECT * FROM users WHERE username = :username AND password = :password")
            result = conn.execute(query, {"username": username, "password": password}).fetchone()
            conn.close()
            return result is not None  # True if user exists
        except Exception as e:
            st.error(f"Authentication error: {e}")
    return False

# ------------------------------- #
# LOGIN PAGE
# ------------------------------- #
def login_page():
    st.title("Login to Task Management App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["authenticated"] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# ------------------------------- #
# SYSTEM REFRESH PAGE
# ------------------------------- #
def system_refresh_page():
    st.header("System Refresh Task")
    task_type = st.selectbox("Select Task Type", ["Refresh", "Complete"])
    additional_input = st.text_input("Enter Additional Input (e.g., IP Address)")

    if st.button("Execute Task"):
        if additional_input:
            st.success(f"Task '{task_type}' executed with input: {additional_input}")
        else:
            st.warning("Please provide additional input.")

# ------------------------------- #
# FUNCTION TO FETCH SCHEMAS
# ------------------------------- #
def get_schema_names():
    conn = get_db_connection()
    if conn:
        try:
            result = conn.execute(text("SELECT schema_name FROM information_schema.schemata"))
            schemas = [row[0] for row in result.fetchall()]
            conn.close()
            return schemas
        except Exception as e:
            st.error(f"Error fetching schemas: {e}")
            return []
    else:
        return []

# ------------------------------- #
# FUNCTION TO FETCH TABLE NAMES FOR A SELECTED SCHEMA
# ------------------------------- #
def get_table_names(schema):
    conn = get_db_connection()
    if conn:
        try:
            query = text(f"SELECT table_name FROM information_schema.tables WHERE table_schema=:schema")
            result = conn.execute(query, {"schema": schema})
            tables = [row[0] for row in result.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            st.error(f"Error fetching table names: {e}")
            return []
    else:
        return []
# ------------------------------- #
# MAIN APPLICATION
# ------------------------------- #
def main():
    # Session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Check if the user is authenticated
    if not st.session_state["authenticated"]:
        login_page()
        return

    # Sidebar navigation
    st.sidebar.title("Task Management Tool")
    menu = st.sidebar.radio("Navigation", ["System Refresh", "Database View", "Logout"])

    if menu == "System Refresh":
        system_refresh_page()
    elif menu == "Database View":
        database_view_page()
    elif menu == "Logout":
        # Reset session state and clear UI
        st.session_state.clear()
        st.write("You have been logged out. Please refresh the page to log in again.")
        st.stop()
def get_table_names():
    conn = get_db_connection()
    if conn:
        try:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            st.error(f"Error fetching table names: {e}")
            return []
    else:
        return []

# Run the app
if __name__ == "__main__":
    main()
