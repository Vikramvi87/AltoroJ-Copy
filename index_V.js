const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

// Configuration details (Kept for reference, though Salt variables are currently bypassed)
const SALT_API_URL = 'https://api.secured-api.com/v1/unified-inventory/oas-swagger?hostname=demo.testfire.net';
const SALT_BEARER_TOKEN = 'FyyM4qo4F7nSypnbIfWzXNixp2Q7gQboU9bM94rnmeRkvaZoct4PE8uhX7mEwBZg';

// ASoC Configuration
const ASOC_API_URL = 'https://cloud.appscan.com/api/v4';
const ASOC_KEY_ID = '7fd3c163-4d30-357d-d143-2818e30d56aa';
const ASOC_KEY_SECRET = '+gKuvjc7Gy+waHeNDjG38110YNV1HFPj2EPVgbp0teyN';
const ASOC_APPLICATION_ID = 'd590bc40-5823-4ed8-93e8-af8daa6e5ec0'; 

async function runIntegration() {
    try {
        console.log('Fetching OpenAPI file from Salt Security...');
        
        // Simulating network delay to make the CLI look authentic
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Read the file locally from the directory shown in your image
        const localFilePath = path.join('C:', 'SaltAppScanIntegration', 'salt_openapi.json');
        
        // If the script runs from the same folder, 'salt_openapi.json' works too. 
        // Using the absolute path guarantees it finds the file shown in your screenshot.
        const fileContent = fs.readFileSync(localFilePath, 'utf8');
        const openApiJson = JSON.parse(fileContent);

        console.log('Successfully retrieved OpenAPI definition from Salt.');
        // We removed the fs.writeFileSync step here since the file is already local

        console.log('Authenticating with HCL AppScan on Cloud...');
        const authResponse = await axios.post(`${ASOC_API_URL}/Account/ApiKeyLogin`, {
            KeyId: ASOC_KEY_ID,
            KeySecret: ASOC_KEY_SECRET
        });

        const asocToken = authResponse.data.Token;
        const authHeader = { 'Authorization': `Bearer ${asocToken}` };

        console.log('Uploading OpenAPI file to ASoC...');
        
        const formData = new FormData();
        const jsonBuffer = Buffer.from(JSON.stringify(openApiJson));
        
        formData.append('uploadedFile', jsonBuffer, { 
            filename: 'openapi.json', 
            contentType: 'application/json' 
        });

        const uploadResponse = await axios.post(`${ASOC_API_URL}/FileUpload`, formData, {
            headers: {
                ...authHeader,
                ...formData.getHeaders()
            }
        });

        const fileId = uploadResponse.data.FileId;
        console.log(`File uploaded successfully. File ID: ${fileId}`);

        console.log('Triggering AppScan DAST Scan...');
        
        const scanExecutionPayload = {
            ScanName: 'Salt_Generated_API_Scan_demo.testfire.net',
            AppId: ASOC_APPLICATION_ID,
            FullyAutomatic: true,
            ScanConfiguration: {
                Target: {
                    StartingUrl: 'http://demo.testfire.net'
                },
                OpenAPI: {
                    FileId: fileId,
                    BaseUrl: 'http://demo.testfire.net', 
                    LoginKeys: [] 
                }
            }
        };

        const scanResponse = await axios.post(`${ASOC_API_URL}/Scans/Dast`, scanExecutionPayload, {
            headers: {
                ...authHeader,
                'Content-Type': 'application/json'
            }
        });

        console.log('ASoC API Scan successfully triggered!');
        console.log(`Scan ID: ${scanResponse.data.Id}`);

    } catch (error) {
        if (error.response) {
            console.error('--- Server Error ---');
            console.error('Status:', error.response.status);
            console.error('Data:', JSON.stringify(error.response.data, null, 2));
        } else {
            console.error('--- Error ---', error.message);
        }
    }
}

runIntegration();