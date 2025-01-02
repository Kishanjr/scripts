import streamlit as st
import mysql.connector
import pandas as pd

# ------------------------------- #
# DATABASE CONNECTION SETTINGS
# ------------------------------- #
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # Replace with your DB username
    "password": "password",  # Replace with your DB password
    "database": "mydb"       # Replace with your database name
}

# ------------------------------- #
# DATABASE CONNECTION FUNCTION
# ------------------------------- #
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# ------------------------------- #
# USER AUTHENTICATION FUNCTION
# ------------------------------- #
def authenticate_user(username, password):
    # Replace with secure DB validation
    return username == "admin" and password == "password123"

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
            st.experimental_rerun()
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
# DATABASE VIEW PAGE
# ------------------------------- #
def database_view_page():
    st.header("Database View")
    conn = get_db_connection()
    if conn:
        query = "SELECT * FROM my_table"  # Replace with your table name
        df = pd.read_sql(query, conn)
        st.dataframe(df)  # Display the table in a DataFrame
        conn.close()

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
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()
