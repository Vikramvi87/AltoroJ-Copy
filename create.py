import requests
import json
import sys

# The ASoC REST APIs used in this script:
REST_APIKEYLOGIN = "https://cloud.appscan.com/api/v4/Account/ApiKeyLogin"
REST_ASSETGROUPS = "https://cloud.appscan.com/api/v4/AssetGroups"
REST_APPS = "https://cloud.appscan.com/api/v4/Apps"

# Hardcoded credentials and application name
keyid = "9c2c7b23-9b4d-8429-ff3b-737ae91aeb3a"
keysecret = "9qENS0oUsuJj8dZ0TxNNTQKJUdUC1c1W8/WjJYv5KFZ6"
appName = "TTT"

def main():
    # login to ASoC and get the bearer token
    token = getToken(keyid, keysecret)

    # Create asset group and get its ID
    assetGroupId = createAssetGroup(token, "Default Asset Group")

    # Create the app and return the ID
    appId = createApp(token, assetGroupId, appName)
    print(appId)

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
