import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import socket

# File with drive credentials
creds_file = "service_account.json"
# ID of google drive folder -> what shows up in url after /folders/<here>
drive_folder_id = "10I7K-fN_rdrXimnhK21OqjeOgO4Ymhln"

# name of file to store in drive
write_filename = "rpi_a.txt"


def authenticate_google_drive(creds_file):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def get_public_ip_address():
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json().get('ip')
    return ip_address

def get_private_ip_address():
    try:
        # Connect to a remote server; no actual data will be sent.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS address is used for reachability
        ip_address = s.getsockname()[0]  # Retrieve local IP address used in this connection
        s.close()
        return ip_address
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def upload_file_drive(drive_service, drive_folder_id, file_name):
    # Get file if it already exists
    query = f"'{drive_folder_id}' in parents and name='{file_name}' and trashed=false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = results.get('files', [])
    existing_file = files[0] if files else None
    
    # If the file exists, delete it
    if existing_file:
        drive_service.files().delete(fileId=existing_file['id']).execute()

    # Upload new file
    file_metadata = {
        # I bet this filename is what it gets called in drive
        'name': file_name,
        'mimeType': 'text/plain',
        'parents': [drive_folder_id]
    }

    # NOTE: I bet if we change the filename here, we can pick which file we want
    #  it to upload
    media = MediaFileUpload(file_name, mimetype='text/plain')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    file_id = file.get('id')
    print(f"File created on Google Drive with ID: {file_id}")

def main():
    drive_service = authenticate_google_drive(creds_file)

    ip_addr = get_private_ip_address()

    with open(write_filename, "w") as file:
        file.write(ip_addr)

    upload_file_drive(drive_service, drive_folder_id, write_filename)


if __name__ == '__main__':
    main()
