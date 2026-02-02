import requests
import json
import sys
import pandas as pd

# The ASoC REST APIs used in this script:
REST_APIKEYLOGIN = "https://cloud.appscan.com/api/v4/Account/ApiKeyLogin"
REST_ASSETGROUPS = "https://cloud.appscan.com/api/v4/AssetGroups"
REST_APPS = "https://cloud.appscan.com/api/v4/Apps"

# Hardcoded credentials
keyid = "348a6a9b-fb71-7ea0-eb3c-8c54309a07b0"
keysecret = "9qlHX4P6x+YvGu3/RWUXfhX6ayf1s+TZc41omhUngF5M"

def main():
    # login to ASoC and get the bearer token
    token = getToken(keyid, keysecret)

    # Read the Excel file
    df = pd.read_excel('VVVV.xlsx')

    for index, row in df.iterrows():
        assetGroupName = row['Asset Group']
        appName = row['UAT_PROJECT']

        # Check if asset group already exists
        assetGroupId = getAssetGroupId(token, assetGroupName)
        if not assetGroupId:
            # Create asset group and get its ID
            assetGroupId = createAssetGroup(token, assetGroupName)

        # Check if application already exists
        appId = getAppId(token, appName)
        if not appId:
            # Create the app and return the ID
            appId = createApp(token, assetGroupId, appName)
            print(f"Created app {appName} with ID {appId} in asset group {assetGroupName}")
        else:
            print(f"Application {appName} already exists with ID {appId}. Assigned to asset group {assetGroupName}")

def getToken(keyId, keySecret):
    try:
        jsonData = {"KeyId": keyId, "KeySecret": keySecret}
        request = requests.post(REST_APIKEYLOGIN, json=jsonData)
        if request.status_code != 200:
            print("Error: Unsuccessful call to " + REST_APIKEYLOGIN + ", Status Code=" + str(request.status_code) + "\n" + request.text)
            sys.exit(1)
        jsonData = json.loads(request.text)
        return jsonData['Token']
    except requests.exceptions.RequestException as e:
        print("Error in getToken():\n" + str(e))
        sys.exit(1)

def getAssetGroupId(token, assetGroupName):
    try:
        headers = {"Authorization": "Bearer " + token}
        request = requests.get(REST_ASSETGROUPS, headers=headers)
        if request.status_code != 200:
            print("Error in getAssetGroupId(): Unsuccessful call to " + REST_ASSETGROUPS + ", Status Code=" + str(request.status_code) + "\n" + request.text)
            sys.exit(1)
        assetGroups = json.loads(request.text)
        for assetGroup in assetGroups['Items']:
            if assetGroup['Name'] == assetGroupName:
                return assetGroup['Id']
        return None
    except requests.exceptions.RequestException as e:
        print("Error in getAssetGroupId():\n" + str(e))
        sys.exit(1)

def getAppId(token, appName):
    try:
        headers = {"Authorization": "Bearer " + token}
        request = requests.get(REST_APPS, headers=headers)
        if request.status_code != 200:
            print("Error in getAppId(): Unsuccessful call to " + REST_APPS + ", Status Code=" + str(request.status_code) + "\n" + request.text)
            sys.exit(1)
        apps = json.loads(request.text)
        for app in apps['Items']:
            if app['Name'] == appName:
                return app['Id']
        return None
    except requests.exceptions.RequestException as e:
        print("Error in getAppId():\n" + str(e))
        sys.exit(1)

def createAssetGroup(token, assetGroupName):
    try:
        headers = {"Authorization": "Bearer " + token}
        jsonData = {"Name": assetGroupName}
        request = requests.post(REST_ASSETGROUPS, headers=headers, json=jsonData)
        if request.status_code != 201:
            print("Error in createAssetGroup(): Unsuccessful call to " + REST_ASSETGROUPS + ", Status Code=" + str(request.status_code) + "\n" + request.text)
            sys.exit(1)
        jsonData = json.loads(request.text)
        return jsonData['Id']
    except requests.exceptions.RequestException as e:
        print("Error in createAssetGroup():\n" + str(e))
        sys.exit(1)

def createApp(token, assetGroupId, appName):
    try:
        headers = {"Authorization": "Bearer " + token}
        jsonData = {"Name": appName, "AssetGroupId": assetGroupId}
        request = requests.post(REST_APPS, headers=headers, json=jsonData)
        if request.status_code != 201:
            print("Error in createApp(): Unsuccessful call to " + REST_APPS + ", Status Code=" + str(request.status_code) + "\n" + request.text)
            sys.exit(1)
        jsonData = json.loads(request.text)
        return jsonData['Id']
    except requests.exceptions.RequestException as e:
        print("Error in createApp():\n" + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
