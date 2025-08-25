import requests
import json

def main():
    """
    Main function to handle AppScan API login and scan initiation.
    """
    # Define the login API endpoint and credentials
    login_url = "https://cloud.appscan.com/api/v4/Account/ApiKeyLogin"
    # IMPORTANT: Replace with your actual Key ID and Key Secret
    key_id = "7fd3c163-4d30-357d-d143-2818e30d56aa"
    key_secret = "+gKuvjc7Gy+waHeNDjG38110YNV1HFPj2EPVgbp0teyN"

    # Create the login payload
    login_payload = {
        "keyId": key_id,
        "keySecret": key_secret
    }

    # Set up the headers for login request
    login_headers = {
        "Content-Type": "application/json"
    }

    print("Attempting to log in to AppScan...")
    # Make the API request to log in
    try:
        login_response = requests.post(login_url, headers=login_headers, data=json.dumps(login_payload))
        login_response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        print("Login successful!")
        access_token = login_response.json().get("Token")
        if access_token:
            print(f"Access Token retrieved (first 5 chars): {access_token[:5]}...")
        else:
            print("Access Token not found in login response.")
            print(f"Login Response: {login_response.json()}")
            return

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred during login: {http_err}")
        try:
            print(f"Login Response Body: {login_response.json()}")
        except json.JSONDecodeError:
            print(f"Login Response Body (raw): {login_response.text}")
        return
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during login: {req_err}")
        return


    def generate_repo_token(token):
        """
        Function to generate a repository signature token for GitHub.
        """
        repo_token_url = "https://cloud.appscan.com/api/v4/Scans/RepoSignature/GitHub"
        # Ensure this URL is correct for your GitHub repository
        repo_url = "https://github.com/Vikramvi87/AltoroJ-Copy.git"
        repo_payload = {
            "url": repo_url
        }
        repo_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        print(f"\nAttempting to generate repository token for {repo_url}...")
        try:
            repo_response = requests.post(repo_token_url, headers=repo_headers, data=json.dumps(repo_payload))
            repo_response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

            repo_signature = repo_response.json().get("repoSignature")
            if repo_signature:
                print("Repository token generated successfully.")
                return repo_signature
            else:
                print("RepoSignature not found in response.")
                print(f"Repo Token Response: {repo_response.json()}")
                return None
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while generating repo token: {http_err}")
            try:
                print(f"Repo Token Response Body: {repo_response.json()}")
            except json.JSONDecodeError:
                print(f"Repo Token Response Body (raw): {repo_response.text}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred while generating repo token: {req_err}")
            return None


    # Generate the repository token
    repo_signature = generate_repo_token(access_token)
    if not repo_signature:
        print("Exiting as repository token could not be generated.")
        return

    # Define the scan API endpoint and details
    api_url = "https://cloud.appscan.com/api/v4/scans/Sast"
    # IMPORTANT: Replace with your actual Application ID
    application_id = "d590bc40-5823-4ed8-93e8-af8daa6e5ec0"
    repository_url = "https://github.com/Vikramvi87/AltoroJ-Copy.git"
    scan_name = "MyAutomatedSastScan"  # A descriptive scan name
    # IMPORTANT: Ensure this is the correct Application File ID if different from application_id
    application_file_id = "d590bc40-5823-4ed8-93e8-af8daa6e5ec0"

    # Create the scan payload
    payload = {
        "applicationId": application_id,
        "scanName": scan_name,
        "scanType": "Static", # For SAST, scanType is typically "Static"
        "sourceType": "Git",
        "source": {
            "url": repository_url
        },
        # applicationFileId is used for specific file/build uploads in some SAST configurations.
        # If your scan doesn't require a specific file ID, you might omit this or ensure it's correct.
        "applicationFileId": application_file_id,
        "repositoryDetails": {
            "url": repository_url,
            # CRITICAL CORRECTION: Ensure owner matches the GitHub username exactly
            "owner": "Vikramvi87",
            "repoName": "AltoroJ-Copy",
            "repoSignature": repo_signature  # Use the generated repo signature
        }
    }

    # Set up the headers with authentication using access token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    print("\nAttempting to start SAST scan...")
    # Make the API request to start the scan
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        print("Scan started successfully!")
        scan_id = response.json().get("id")
        if scan_id:
            print(f"Scan ID: {scan_id}")
        else:
            print("Scan ID not found in response.")
            print(f"Scan Start Response: {response.json()}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while starting scan: {http_err}")
        try:
            print(f"Scan Start Response Body: {response.json()}")
        except json.JSONDecodeError:
            print(f"Scan Start Response Body (raw): {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred while starting scan: {req_err}")

if __name__ == "__main__":
    main()
