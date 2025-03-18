import streamlit as st
import paramiko
import json

def execute_query_script(host, port, username, password, script_path):
    # Create an SSH client
    client = paramiko.SSHClient()
    # Automatically add the server's SSH key (for development only)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server with provided credentials
        client.connect(hostname=host, port=port, username=username, password=password)
        
        # Execute the query.sh script
        # Using "bash" ensures the script is executed correctly even if not executable.
        command = f"bash {script_path}"
        stdin, stdout, stderr = client.exec_command(command)

        # Get the command output and error
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error:
            return f"Error executing script: {error}"

        # Attempt to parse output as JSON
        try:
            data = json.loads(output)
            return data
        except json.JSONDecodeError:
            return output

    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        client.close()

def main():
    st.title("Remote query.sh Script Executor")

    # Create a form to get server details and script path from the user
    with st.form("server_form"):
        st.subheader("Enter Server Details")
        host = st.text_input("Server IP", value="192.168.1.100")
        port = st.number_input("SSH Port", value=22)
        username = st.text_input("Username", value="your_username")
        password = st.text_input("Password", type="password")
        script_path = st.text_input("Path to query.sh", value="/path/to/query.sh")
        submitted = st.form_submit_button("Execute Script")
    
    if submitted:
        st.info("Executing the script on the server...")
        result = execute_query_script(host, port, username, password, script_path)
        
        st.subheader("Result")
        # Check if result is JSON-parsable
        if isinstance(result, dict) or isinstance(result, list):
            st.json(result)
        else:
            st.text(result)

if __name__ == "__main__":
    main()
