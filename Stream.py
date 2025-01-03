import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

# ------------------------------- #
# DATABASE CONNECTION SETTINGS
# ------------------------------- #
DB_CONFIG = {
    "user": "postgres",
    "password": "password",  # Replace with your actual password
    "host": "localhost",
    "port": "5432",
    "database": "mydb"
}

# Creating a SQLAlchemy engine for PostgreSQL connection
engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

# ------------------------------- #
# USER AUTHENTICATION FUNCTION
# ------------------------------- #
def authenticate_user(username, password):
    """Authenticate user using the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT * FROM users WHERE username = :username AND password = :password"),
                {"username": username, "password": password}
            ).fetchone()
            return result is not None
    except Exception as e:
        st.error(f"Database error during authentication: {e}")
        return False

# ------------------------------- #
# LOGIN PAGE
# ------------------------------- #
def login_page():
    """Render the login page."""
    st.title("🔐 Secure Login")
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login", type="primary"):
        if authenticate_user(username, password):
            st.session_state["authenticated"] = True
            st.success("✅ Successfully logged in!")
        else:
            st.error("❌ Invalid username or password!")

# ------------------------------- #
# SYSTEM REFRESH TASK PAGE
# ------------------------------- #
def system_refresh_page():
    """Page to execute a system refresh task."""
    st.header("🛠️ System Refresh Task")
    task_type = st.selectbox("Select Task Type", ["Refresh", "Complete"])
    additional_input = st.text_input("Enter Additional Input (e.g., IP Address)")

    if st.button("Execute Task"):
        if additional_input:
            st.success(f"✅ Task '{task_type}' executed with input: {additional_input}")
        else:
            st.warning("⚠️ Please provide the additional input!")

# ------------------------------- #
# DATABASE VIEW PAGE
# ------------------------------- #
def database_view_page():
    """Page to view data from the PostgreSQL database."""
    st.header("📊 Database View")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM my_table"))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            st.dataframe(df)
    except Exception as e:
        st.error(f"Database error: {e}")

# ------------------------------- #
# MAIN APPLICATION FUNCTION
# ------------------------------- #
def main():
    """Main function to control the Streamlit application."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # If user is not authenticated, show the login page
    if not st.session_state["authenticated"]:
        login_page()
        return

    # Sidebar navigation for different pages
    st.sidebar.title("📂 Task Management Tool")
    menu = st.sidebar.radio("Navigation", ["System Refresh", "Database View", "Logout"])

    if menu == "System Refresh":
        system_refresh_page()
    elif menu == "Database View":
        database_view_page()
    elif menu == "Logout":
        st.session_state.clear()
        st.success("✅ You have been logged out. Please refresh the page.")
        st.stop()

# ------------------------------- #
# Run the Streamlit App
# ------------------------------- #
if __name__ == "__main__":
    main()
