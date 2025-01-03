# ------------------------------- #
# PAGE: RUN CUSTOM QUERY BY ORDER NUMBER
# ------------------------------- #
def custom_query_page():
    st.header("Search Order by Order Number")
    order_number = st.text_input("Enter Order Number")

    if st.button("Search"):
        if order_number:
            try:
                result = run_custom_query(order_number)
                if not result.empty:
                    st.dataframe(result)
                else:
                    st.warning("No records found for the given order number.")
            except Exception as e:
                st.error(f"Error fetching data: {e}")
        else:
            st.warning("Please enter a valid order number.")
# ------------------------------- #
# FUNCTION TO RUN CUSTOM QUERY BY ORDER NUMBER
# ------------------------------- #
def run_custom_query(order_number):
    conn = get_db_connection()
    if conn:
        try:
            query = text(f"SELECT * FROM sales.orders WHERE order_id = :order_number")
            result = pd.read_sql(query, conn, params={"order_number": order_number})
            conn.close()
            return result
        except Exception as e:
            st.error(f"Error executing query: {e}")
            conn.close()
            return None
    return None

# ------------------------------- #
# PAGE: DATABASE VIEW WITH COLUMN SELECTION AND SAVING VIEWS
# ------------------------------- #
def database_view_page():
    st.header("Database View with Column Selection")

    # Select Schema
    schemas = get_schema_names()
    selected_schema = st.selectbox("Select Schema:", schemas)

    # Select Table
    if selected_schema:
        tables = get_table_names(selected_schema)
        selected_table = st.selectbox("Select Table:", tables)

        # Select Columns
        if selected_table:
            columns = get_column_names(selected_schema, selected_table)
            selected_columns = st.multiselect("Select Columns:", columns)

            # Show Selected Data
            if st.button("Show Selected Data"):
                conn = get_db_connection()
                if conn:
                    try:
                        query = text(f'SELECT {", ".join(selected_columns)} FROM "{selected_schema}"."{selected_table}" LIMIT 10')
                        df = pd.read_sql(query, conn)
                        st.dataframe(df)
                    except Exception as e:
                        st.error(f"Error displaying data: {e}")
                    finally:
                        conn.close()
