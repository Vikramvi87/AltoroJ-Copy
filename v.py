import requests
import json
import time

# Define the API endpoints and credentials
login_url = "https://cloud.appscan.com/api/v4/Account/ApiKeyLogin"
sast_scan_url = "https://cloud.appscan.com/api/v4/Scans/SAST"
key_id = "7fd3c163-4d30-357d-d143-2818e30d56aa"
key_secret = "+gKuvjc7Gy+waHeNDjG38110YNV1HFPj2EPVgbp0teyN"
owner = "Vikramvi87"
repo_name = "AltoroJ-Copy"
scan_name = "MyScan"
application_file_id = "d590bc40-5823-4ed8-93e8-af8daa6e5ec0"
repo_signature = "133947958968462670:LQ5JGRfGqtKuHHGXNdMDDMtfekxnMtpjyX1g7UyWCoI="

# Create the payload for login
login_payload = {
    "KeyId": key_id,
    "KeySecret": key_secret
}

# Set up the headers
headers = {
    "Content-Type": "application/json"
}

# Make the API request to login
login_response = requests.post(login_url, headers=headers, data=json.dumps(login_payload))

# Check the response
if login_response.status_code == 200:
    auth_token = login_response.json().get("Token")
    print(f"Login successful. Auth Token: {auth_token}")
    print("Login Response:", login_response.json())

    # Update headers with the auth token
    headers["Authorization"] = f"Bearer {auth_token}"

    # Create the payload for SAST scan
    sast_payload = {
        "ScanName": scan_name,
        "EnableMailNotification": True,
        "Locale": "en-US",
        "AppId": application_file_id,
        "Execute": True,
        "FullyAutomatic": True,
        "Personal": True,
        "Comment": "Initial scan",
        "RepositoryDetails": {
            "RepoSignature": repo_signature,
            "Owner": owner,
            "RepoName": repo_name,
            "BranchName": "master",
            "Platform": "GitHub"
        },
        "Recurrence": {
            "Rule": "0 0 * * 1",  # Cron format for weekly recurrence on Monday at midnight
            "StartDate": "2025-06-19T00:00:00Z",
            "EndDate": "2025-12-31T00:00:00Z"
        },
        "scanModel": "default"
    }

    # Make the API request to initiate the SAST scan
    sast_response = requests.post(sast_scan_url, headers=headers, data=json.dumps(sast_payload))

    # Check the response
    if sast_response.status_code in [200, 201]:
        scan_id = sast_response.json().get("ScanId", sast_response.json().get("Id"))
        print(f"SAST Scan initiated successfully. Scan ID: {scan_id}")
        print("SAST Response:", sast_response.json())
    elif sast_response.status_code == 403:
        print("Forbidden request. Please check your repository signature.")
        print("SAST Response:", sast_response.json())
    elif sast_response.status_code == 401:
        print("Unauthorized request. Please check your key ID and key secret.")
        print("SAST Response:", sast_response.json())
    else:
        print(f"Failed to initiate SAST scan: {sast_response.status_code}")
        try:
            print("SAST Response:", sast_response.json())
        except json.JSONDecodeError:
            print("SAST Response Text:", sast_response.text)
else:
    print(f"Failed to login: {login_response.status_code}")
    try:
        print("Login Response:", login_response.json())
    except json.JSONDecodeError:
        print("Login Response Text:", login_response.text)
