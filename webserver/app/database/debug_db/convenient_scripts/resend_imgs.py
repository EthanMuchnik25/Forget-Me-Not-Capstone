# This script exists if you have a directory full of images, and want to send
#  them all to a user's storage as though you were a raspi camera. This is 
#  up-to-date as of implementing auth for the first time (10/21)

# This can be run from anywhere, just make sure you have the correct things pip 
#  installed, and have the server url set correctly (diff if you're in docker 
#  container)

import os
import requests

# NOTE: This is copy pasted from img_send.py, but I am too lazy to make the code
#  modular. I could make an "auth" module, but this seems painful

server_url = "http://localhost:4000"

img_url = server_url + "/post_img"
token = ""
# Credentials of account you want to send to 
uname = "a"
pw = "a"
# Initially no token, just re-authenticate the first time
token = ""

img_directory = '../../debug_db_store/prev/old_imgs'


def reauthenticate():
    global uname
    global pw
    global token
    login_url = server_url + "/login"
    payload = {
        'username': uname,
        'password': pw
        }
    response = requests.post(login_url, json=payload)

    if response.status_code == 200:
        print('Login successful!')
        print('Access token:', response.json().get('access_token'))

        token = response.json().get('access_token')
        return True
    elif response.status_code == 400:
        print('Login failed:', response.json().get('msg'))
    else:
        print('Unexpected error:', response.status_code, response.text)
    return False

# Note: This takes a file handle, not a path
def send_img_req(img_file):
    global token
    global img_url

    files = {'file': img_file}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(img_url, headers=headers, files=files)
    if response.status_code == 200:
        return

    print(f"error sending image: {response.status_code}  Response: {response.text}")
    print("Attempting reauthentication")

    # Case code 401, unauthenticated
    
    if not reauthenticate():
        raise Exception("Failed to reauthenticate")

    img_file.seek(0)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(img_url, headers=headers, files=files)
    if response.status_code != 200:
        print(f"Failed to send after reauthentication: {response.status_code}  Response: {response.text}")


def traverse_and_send_images(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as file:
                    send_img_req(file)


if __name__ == "__main__":
    traverse_and_send_images(img_directory)
