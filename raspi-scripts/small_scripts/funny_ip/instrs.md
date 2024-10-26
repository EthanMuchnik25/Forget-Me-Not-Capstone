# Big instructions - how to set up cloud stuff

If you only have access to the command line and need to avoid the OAuth consent screen (which requires a browser), you can use a **service account** to authenticate with Google Drive. Service accounts are intended for server-to-server interactions and don’t require user consent via a browser window, making them perfect for command-line only environments.

Here's how you can modify the script to work with a service account.

### 1. Set Up a Service Account with Google Drive API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and make sure you're logged into your project.
2. Navigate to **APIs & Services > Credentials**.
3. Click **Create Credentials** and select **Service Account**.
4. Fill out the required details, then proceed to create the service account.
5. In the **Service Account** details, go to the **Keys** section, click **Add Key**, and choose **JSON**. This will download a JSON file with the service account credentials. Save this file to your project folder, and name it something like `service_account.json`.

6. **Set Permissions**: The service account needs access to your Google Drive:
   - Share a folder with the service account’s email address (found in the JSON file, e.g., `my-service-account@my-project.iam.gserviceaccount.com`).
   - You can create a folder in your Google Drive and share it with this email address to give it edit access. Any files the service account uploads should be placed within this shared folder.

### 2. Modify the Python Script to Use the Service Account

Here’s how to modify the original script to use the service account credentials.

```python
import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API setup using service account
def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

# Get public IP address
def get_ip_address():
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json().get('ip')
    return ip_address

# Create or update IP address file on Google Drive
def upload_ip_address(drive_service, file_id=None):
    ip_address = get_ip_address()
    file_name = "ip_address.txt"

    # Write IP address to a file
    with open(file_name, 'w') as file:
        file.write(f"My public IP address is: {ip_address}\n")

    # Check if file exists, if not, create it
    if file_id is None:
        file_metadata = {
            'name': file_name,
            'mimeType': 'text/plain'
        }
        media = MediaFileUpload(file_name, mimetype='text/plain')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        print(f"File created on Google Drive with ID: {file_id}")
    else:
        # Update existing file
        media = MediaFileUpload(file_name, mimetype='text/plain')
        file = drive_service.files().update(fileId=file_id, media_body=media).execute()
        print("File updated on Google Drive.")

    return file_id

# Main function to run the upload
def main():
    # Authenticate with Google Drive
    drive_service = authenticate_google_drive()

    # Track the file ID (if re-running the script multiple times)
    file_id_path = "file_id.json"
    if os.path.exists(file_id_path):
        with open(file_id_path, 'r') as f:
            file_id = json.load(f).get('file_id')
    else:
        file_id = None

    # Upload the IP address
    file_id = upload_ip_address(drive_service, file_id)

    # Save the file ID for future updates
    with open(file_id_path, 'w') as f:
        json.dump({'file_id': file_id}, f)

if __name__ == '__main__':
    main()
```

### Explanation of Modifications

- **Service Account Authentication**: The `authenticate_google_drive` function now uses the `service_account.Credentials.from_service_account_file` method, which authenticates directly with the service account JSON file.
- **Folder Sharing**: Since you don’t have a direct Google Drive account for this service account, you need to **share a folder** in your main Google Drive with the service account’s email. Place the file in this shared folder so you can see it on Google Drive.

### Running the Script

1. Place the `service_account.json` file in the same directory as the script.
2. Run the script:
   ```bash
   python upload_ip_to_drive.py
   ```

This will create a text file with the IP address in your Google Drive folder or update it if it already exists, all from the command line without needing a browser-based authentication flow.



# Additional script modify to get folder we want

To see the file uploaded by the service account to Google Drive, you need to access it through the shared folder in your personal Google Drive, where you granted access to the service account. Here’s how:

### Step 1: Share a Folder in Your Google Drive with the Service Account
1. Go to [Google Drive](https://drive.google.com/) and create a new folder (e.g., `IP Addresses`).
2. Right-click the folder, select **Share**, and enter the service account's email address (found in the `service_account.json` file, e.g., `my-service-account@my-project.iam.gserviceaccount.com`).
3. Set the permission to **Editor**, so the service account can upload files into this folder.

### Step 2: Update Your Script to Upload Files to the Shared Folder
Now that the service account has access to the shared folder, we’ll need to modify the script slightly to make sure the file is uploaded into this specific folder.

1. **Get the Folder ID**: 
   - Open the shared folder in your browser.
   - Copy the **Folder ID** from the URL. It will look like this:
     ```
     https://drive.google.com/drive/folders/<FOLDER_ID>
     ```

2. **Update the Script** to upload to this folder by adding the folder ID to `file_metadata`:
   ```python
   def upload_ip_address(drive_service, file_id=None):
       ip_address = get_ip_address()
       file_name = "ip_address.txt"

       # Write IP address to a file
       with open(file_name, 'w') as file:
           file.write(f"My public IP address is: {ip_address}\n")

       # Specify the folder ID in file metadata to upload to the shared folder
       folder_id = "<FOLDER_ID>"  # Replace with your folder ID
       file_metadata = {
           'name': file_name,
           'mimeType': 'text/plain',
           'parents': [folder_id]
       }
       ...
   ```

3. **Run the Script Again** to ensure the file uploads to the shared folder.

### Step 3: View the File
1. Go to Google Drive and open the shared folder.
2. You should see `ip_address.txt` within the folder, containing the computer’s IP address. 

Each time the script runs, it will upload or update the file within this shared folder, making it easy to find.