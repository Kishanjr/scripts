import paramiko
import json

def execute_query_script(host, port, username, password, script_path):
    # Create an SSH client
    client = paramiko.SSHClient()
    # Automatically add the server's SSH key (for testing; consider a stricter policy for production)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server using the provided credentials
        client.connect(hostname=host, port=port, username=username, password=password)
        print("Connected to the server successfully!")

        # Execute the query.sh script. If it's executable, you can run it directly.
        # Alternatively, you can run "bash query.sh" if needed.
        command = f"bash {script_path}"
        stdin, stdout, stderr = client.exec_command(command)

        # Read the output and error streams
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if error:
            print("Error executing script:", error)
            return None

        # Try to parse the output as JSON
        try:
            data = json.loads(output)
            print("Script executed successfully. Parsed JSON data:")
            return data
        except json.JSONDecodeError:
            print("Script executed successfully. Output is not in JSON format. Raw output:")
            return output

    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    # Replace these values with your server's details and script path
    host = "192.168.1.100"          # Server IP address
    port = 22                       # SSH port, usually 22
    username = "your_username"      # Your login username
    password = "your_password"      # Your login password
    script_path = "/path/to/query.sh"  # Full path to your query.sh script on the server

    result = execute_query_script(host, port, username, password, script_path)
    
    if result is not None:
        if isinstance(result, dict) or isinstance(result, list):
            # If JSON data, pretty-print it
            print(json.dumps(result, indent=4))
        else:
            # Otherwise, print the raw output
            print(result)
