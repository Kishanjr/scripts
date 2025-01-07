import streamlit as st
import psycopg2
import pandas as pd

# Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "database": "mydb",
    "user": "postgres",
    "password": "password",
    "port": "5432"
}

# Function to establish a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Function to fetch data from the database based on a selected column
def fetch_data(table_name, column_name):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = f"SELECT id, {column_name} FROM {table_name}"
                cursor.execute(query)
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['id', column_name])
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            conn.close()
            return pd.DataFrame()
    else:
        return pd.DataFrame()

# Function to update a specific value in the database
def update_value(table_name, column_name, new_value, row_id):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = f"UPDATE {table_name} SET {column_name} = %s WHERE id = %s"
                cursor.execute(query, (new_value, row_id))
                conn.commit()
                st.success(f"Updated {column_name} to {new_value} for ID {row_id}")
            conn.close()
        except Exception as e:
            st.error(f"Error updating value: {e}")
            conn.close()

# Streamlit app layout
def main():
    st.title("Hardcoded List Selector and Updater")

    # Define the hardcoded list of options
    options = ['Option A', 'Option B', 'Option C', 'Option D', 'Option E', 'Option F']

    # Select an option from the hardcoded list
    selected_option = st.selectbox("Select an option to update:", options)

    # Input for table name
    table_name = st.text_input("Enter the table name:")

    if table_name and selected_option:
        # Fetch and display data for the selected column
        column_name = selected_option.lower().replace(' ', '_')  # Example transformation
        data = fetch_data(table_name, column_name)
        if not data.empty:
            st.dataframe(data)

            # Inputs for updating a value
            st.subheader("Update a Value")
            row_id = st.number_input("Enter the ID of the row to update:", min_value=1, step=1)
            new_value = st.text_input(f"Enter the new value for {selected_option}:")

            if st.button("Update Value"):
                if new_value:
                    update_value(table_name, column_name, new_value, row_id)
                else:
                    st.warning("Please enter a new value to update.")

if __name__ == "__main__":
    main()
