import requests

# ASoC credentials
key_id = "348a6a9b-fb71-7ea0-eb3c-8c54309a07b0"
key_secret = "9qlHX4P6x+YvGu3/RWUXfhX6ayf1s+TZc41omhUngF5M"

# List of application names
application_names = [
    "Transportal CAS_APM0001226_PROD_CI_OC",
    "Transportal SCMS-Vendor Integration_APM0001227_PROD_CI_OC",
    "NPS_Azure_APM0001167_PROD_CI_OC",
    "Smart verify - Geo Azure_APM0001213_PROD_CI_OC",
    "Service Agreement Portal on Azure Phase -2_APM0001275_PROD_CI_OC",
    "ERT Nomination System_APM0001093_PROD_CI_OC",
    "Voice of Business_APM0002014_PROD_CI_NC",
    "RAS on Azure_APM0001191_PROD_CI_FC",
    "iBadge_APM0001125_PROD_CI_NC",
    "File Upload Component_APM0001098_PROD_CI_NC",
    "Notification Engine_APM0001169_PROD_CI_OC",
    "My Travel TAS AZURE_APM0001163_PROD_CI_FC",
    "My Approvals Azure_APM0001157_PROD_CI_NC",
    "ACSAT(CRISP)_APM0001044_PROD_CI_NC",
    "UPSI Integration Module EDS_Azure_APM0001232_PROD_CI_OC",
    "Common Delegation System_APM0001062_PROD_CI_NC",
    "PDFDocConverter_APM0001401_PROD_CI_NC",
    "Stake Holder Management System (SMS)_APM0001281_PROD_CI_NC",
    "eFacility - HOT Desking Mobile App_APM0002960_PROD_CI_OC",
    "Integration Platform_APM0001130_PROD_CI_NC",
    "Recruitment Invoice Tool_APM0001189_PROD_CI_OC",
    "Application Access Management (AAM)_APM0001047_PROD_CI_OC",
    "OpsHi5_DEI_Azure_APM0001177_PROD_CI_OC",
    "Vendor Service Desk (VSD)_APM0001239_PROD_CI_OC",
    "Digital Client Visit Microsite_APM0001071_PROD_CI_OC"
]

# Authenticate with ASoC using v4 API
auth_url = "https://cloud.appscan.com/api/v4/Account/ApiKeyLogin"
auth_payload = {
    "KeyId": key_id,
    "KeySecret": key_secret
}

try:
    auth_response = requests.post(auth_url, json=auth_payload)
    auth_response.raise_for_status()
    bearer_token = auth_response.json()["Token"]
except requests.exceptions.RequestException as e:
    print(f"Authentication failed: {e}")
    exit(1)

# Get list of applications
headers = {"Authorization": f"Bearer {bearer_token}"}
apps_url = "https://cloud.appscan.com/api/v4/Apps"

try:
    apps_response = requests.get(apps_url, headers=headers)
    apps_response.raise_for_status()
    apps_data = apps_response.json()
    applications = apps_data.get("Items", [])  # Adjust this key if needed
except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve applications: {e}")
    exit(1)

# Map application names to IDs
app_id_map = {app["Name"]: app["Id"] for app in applications if app["Name"] in application_names}

# Print results
for name in application_names:
    print(f"{name}: {app_id_map.get(name, 'Not Found')}")
