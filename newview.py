# ------------------------------- #
# FETCH COLUMN NAMES FOR SELECTED TABLE
# ------------------------------- #
def get_column_names(schema, table):
    conn = get_db_connection()
    if conn:
        try:
            query = text(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema=:schema AND table_name=:table
            """)
            result = conn.execute(query, {"schema": schema, "table": table})
            columns = [row[0] for row in result.fetchall()]
            conn.close()
            return columns
        except Exception as e:
            st.error(f"Error fetching columns: {e}")
            return []
    return []

# ------------------------------- #
# CREATE NEW VIEW BASED ON SELECTION
# ------------------------------- #
def create_view(schema, table, selected_columns, view_name):
    conn = get_db_connection()
    if conn:
        try:
            column_str = ", ".join(selected_columns)
            create_view_query = text(f"""
                CREATE VIEW "{schema}"."{view_name}" AS
                SELECT {column_str} FROM "{schema}"."{table}"
            """)
            conn.execute(create_view_query)
            conn.commit()
            st.success(f"New view '{view_name}' created successfully!")
        except Exception as e:
            st.error(f"Error creating view: {e}")
        finally:
            conn.close()

# ------------------------------- #
# DATABASE VIEW PAGE (WITH COLUMN SELECTION & VIEW CREATION)
# ------------------------------- #
def database_view_page():
    st.header("Database View & Column Selection")

    # Select Schema
    schemas = get_schema_names()
    selected_schema = st.selectbox("Select Schema:", schemas)

    # Select Table
    tables = get_table_names(selected_schema)
    selected_table = st.selectbox("Select Table:", tables)

    # Select Columns
    columns = get_column_names(selected_schema, selected_table)
    selected_columns = st.multiselect("Select Columns to Display:", columns)

    # Preview Data
    if st.button("Show Selected Data"):
        conn = get_db_connection()
        if conn:
            try:
                query = text(f"""
                    SELECT {', '.join(selected_columns)} 
                    FROM "{selected_schema}"."{selected_table}" 
                    LIMIT 10
                """)
                df = pd.read_sql(query, conn)
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error fetching data: {e}")
            finally:
                conn.close()

    # Create a New View
    view_name = st.text_input("Enter New View Name:")
    if st.button("Create View"):
        if selected_columns and view_name:
            create_view(selected_schema, selected_table, selected_columns, view_name)
        else:
            st.warning("Please select columns and provide a view name.")
