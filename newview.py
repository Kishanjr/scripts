import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# ------------------------------- #
# DATABASE CONNECTION SETTINGS
# ------------------------------- #
DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",         
    "password": "password",     
    "database": "mydb",         
    "port": "5432"              
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
        conn = engine.raw_connection()  # Using raw_connection for %s style
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# ------------------------------- #
# FUNCTION TO RUN CUSTOM QUERY USING `%s` (Positional Binding)
# ------------------------------- #
def run_custom_query(order_number):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Using %s safely with a tuple to avoid SQL injection
            query = """
            SELECT 
                request -> 'orderHeader' ->> 'workOrderNumber' AS order_number,
                request -> 'orderHeader' ->> 'orderType' AS order_type,
                request -> 'orderHeader' ->> 'functionCode' AS function_code,
                request -> 'orderHeader' ->> 'workOrderVersion' AS order_version,
                request -> 'orderHeader' ->> 'originatingSystem' AS order_origin,
                transaction_start_time, transaction_end_time
            FROM infra.t_transaction_manager
            WHERE work_order_number = %s
            ORDER BY transaction_end_time DESC
            """
            cursor.execute(query, (order_number,))  # Safely passing input using %s
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return pd.DataFrame(result, columns=columns)
        except Exception as e:
            st.error(f"Error executing the query: {e}")
            conn.close()
            return None
    return None


# ------------------------------- #
# PAGE: RUN CUSTOM QUERY BY ORDER NUMBER
# ------------------------------- #
def custom_query_page():
    st.header("Search Order by Order Number")
    order_number = st.text_input("Enter Order Number")

    if st.button("Search"):
        if order_number:
            result = run_custom_query(order_number)
            if result is not None and not result.empty:
                st.success(f"Results for Order Number: {order_number}")
                st.dataframe(result)
            else:
                st.warning("No records found for the given order number.")
        else:
            st.warning("Please enter a valid order number.")

# ------------------------------- #
# MAIN APPLICATION
# ------------------------------- #
def main():
    st.sidebar.title("Task Management Tool")
    menu = st.sidebar.radio("Navigation", ["Search Order", "Logout"])

    if menu == "Search Order":
        custom_query_page()
    elif menu == "Logout":
        st.session_state.clear()
        st.write("You have been logged out. Please refresh the page to log in again.")
        st.stop()

# Run the app
if __name__ == "__main__":
    main()
