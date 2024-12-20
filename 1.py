import requests

url = "https://connect-voip-provision-kieserver-nts-prod-e0sv.apps-rpod.vpc.verizon.com/services/rest/server/containers/connect-voip-provision/tasks/2728444/states/completed"
headers = {
    "user-connect": "autoprogress=true",
    "accept": "application/json",
    "content-type": "application/json"
}
payload = {
    "isTerminate": False,
    "isRetry": False
}

try:
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 403:
        print("Error: Forbidden (403). Please check the task ID or permissions.")
        print(f"Response body: {response.text}")
    elif response.status_code == 200:
        print("Request successful.")
        print(f"Response body: {response.json()}")
    else:
        print(f"Unexpected status code: {response.status_code}")
        print(f"Response body: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
