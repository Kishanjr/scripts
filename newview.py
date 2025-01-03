# ------------------------------- #
# FUNCTION TO RUN CUSTOM QUERY BY ORDER NUMBER
# ------------------------------- #
def run_custom_query(order_number):
    conn = get_db_connection()
    if conn:
        try:
            query = text(f"""
            WITH message_lines AS (
                SELECT regexp_split_to_table(
                    (SELECT * FROM etl.fn_get_etl_details_by_workorder(:order_number)),
                    E'\n'
                ) AS line
            )
            SELECT
                'domain',
                request -> 'orderHeader' ->> 'workOrderNumber' AS order_number,
                request -> 'orderHeader' ->> 'orderType' AS order_type,
                request -> 'orderHeader' ->> 'functionCode' AS function_code,
                request -> 'orderHeader' ->> 'workOrderVersion' AS order_version,
                request -> 'orderHeader' ->> 'originatingSystem' AS order_origin,
                entity_order_id,
                co_creation_date,
                elem1->>'specValue' AS location_id,
                elem2->>'specValue' AS qos_ind,
                elem3->>'specValue' AS cnam_ind,
                elem4->>'specValue' AS as_id,
                tsi.entity_name AS location_name,
                tsi.entity_type AS location_type,
                (SELECT message_lines.line FROM message_lines 
                 WHERE message_lines.line LIKE '%LOCATION :: Entity ID:%' LIMIT 1),
                request -> 'orderHeader' ->> 'product' AS product,
                request -> 'orderHeader' ->> 'serviceOrderNumber' AS service_order_number,
                request -> 'orderHeader' ->> 'flow' AS flow,
                request -> 'orderHeader' ->> 'rootWorkFlowCaseId' AS root_workflow_case_id,
                substring(transaction_id, 1, 8) AS wfcaseid,
                request -> 'orderHeader' ->> 'workflowCaseId' AS workflow_case_id,
                wf_task_names, status, batch_no,
                request -> 'orderHeader' ->> 'enterpriseId' AS enterprise_id,
                response -> 'responseDetails' ->> 'statusCode' AS resp_status_code,
                response -> 'responseDetails' ->> 'statusDescription' AS resp_status_desc,
                request -> 'orderHeader' ->> 'specification' AS tn_count,
                transaction_start_time, transaction_end_time, response,
                response -> 'entityOrder' AS failure_details
            FROM infra.t_transaction_manager t
            LEFT JOIN ordng.t_master_order o ON o.work_order_number = t.work_order_number
            LEFT JOIN jsonb_array_elements(tmo.master_order_specDetails) elem1 
                ON elem1 ->> 'specName' = 'LOCATION_ID'
            LEFT JOIN svcinv.t_service_inventory tsi 
                ON tsi.entity_id = elem1 ->> 'specValue' 
                AND tsi.entity_type = 'LOCATION'
            LEFT JOIN svcinv.etl_t_service_inventory etsi 
                ON etsi.entity_id = tsi.entity_id
            LEFT JOIN jsonb_array_elements(etsi.entity_attributes) elem2 
                ON elem2 ->> 'specName' = 'QOS_IND'
            LEFT JOIN jsonb_array_elements(etsi.entity_attributes) elem3 
                ON elem3 ->> 'specName' = 'CNAM_IND'
            LEFT JOIN jsonb_array_elements(etsi.entity_attributes) elem4 
                ON elem4 ->> 'specName' = 'AS_ID'
            WHERE o.work_order_number = :order_number
            ORDER BY transaction_end_time DESC
            """)
            
            result = pd.read_sql(query, conn, params={"order_number": order_number})
            conn.close()
            return result
        except Exception as e:
            st.error(f"Error executing the complex query: {e}")
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

# ------------------------------- #
# MAIN APPLICATION
# ------------------------------- #
def main():
    st.sidebar.title("Task Management Tool")
    menu = st.sidebar.radio("Navigation", ["Database View", "Search Order", "Logout"])

    if menu == "Database View":
        database_view_page()
    elif menu == "Search Order":
        custom_query_page()
    elif menu == "Logout":
        st.session_state.clear()
        st.write("You have been logged out. Please refresh the page to log in again.")
        st.stop()

